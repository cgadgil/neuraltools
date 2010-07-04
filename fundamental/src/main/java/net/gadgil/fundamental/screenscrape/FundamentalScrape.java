package net.gadgil.fundamental.screenscrape;

//import java.sql.Date;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TimeZone;
import java.util.logging.Logger;

import javax.management.RuntimeErrorException;

import org.apache.commons.lang.time.DateUtils;
import org.slf4j.LoggerFactory;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import com.gargoylesoftware.htmlunit.BrowserVersion;
import com.gargoylesoftware.htmlunit.Page;
import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.html.HtmlElement;
import com.gargoylesoftware.htmlunit.html.HtmlPage;

public class FundamentalScrape {

	public static List<List<String>> getFinancialDataFromMoneyCentral(
			String symbol, String annualOrQuarterly, String typeOfStatement) {
		WebClient theWebClient = new WebClient(BrowserVersion.FIREFOX_3);
		theWebClient.setJavaScriptTimeout(2000);
		theWebClient.setTimeout(5000);
		theWebClient.setJavaScriptEnabled(false);
		try {
			List<List<String>> theData = new ArrayList<List<String>>();
			theWebClient.setPopupBlockerEnabled(true);
			//theWebClient.setRedirectEnabled(false);
			String theMoneyCentralLink = "http://moneycentral.msn.com/investor/invsub/results/statemnt.aspx?Symbol="
					+ symbol
					+ "&lstStatement="
					+ typeOfStatement
					+ "&stmtView=" + annualOrQuarterly;
			//System.err.println("Downloading data from " + theMoneyCentralLink);
			HtmlPage thePage = theWebClient.getPage(theMoneyCentralLink);
			HtmlElement theHtmlElement = thePage
					.getElementById("StatementDetails");
			List<HtmlElement> theElements = theHtmlElement
					.getElementsByAttribute("table", "class", "ftable");
			HtmlElement theTable = theElements.get(0);
			List<HtmlElement> theRows = theTable.getElementsByTagName("tr");
			for (HtmlElement theRow : theRows) {
				List<HtmlElement> theCells = theRow.getElementsByTagName("td");
				List<String> row = new ArrayList<String>();
				if (theCells.size() != 6) {
					continue;
				}
				for (HtmlElement theCell : theCells) {
					String theText = theCell.getTextContent().replaceAll(",",
							"").trim();
					if (theText.isEmpty() || theText.length() == 1) {
						if (row.size() > 0) {
							LoggerFactory.getLogger("fundamental-analysis")
									.warn("Skipping data for " + row);
						}
						continue;
					}
					// System.out.print(theText + "\t");
					// System.out.println(theText.getBytes());
					row.add(theText);
				}
				if (row.size() == 6) {
					theData.add(row);
					// System.out.println();
				}
			}
			// System.out.println(theHtmlElement);
			return theData;
		} catch (Throwable t) {
			throw new RuntimeException(t);
		} finally {
			theWebClient.closeAllWindows();
		}
	}

	public static void printTabSeparated(List<List<String>> tableData) {
		for (List<String> theRow : tableData) {
			for (String theCell : theRow) {
				System.out.print(theCell + "\t");
			}
			System.out.println("END-OF-LINE");
		}
	}

	public static String readDataFromURL(String url) {
		try {
			URL theURL = new URL(url);
			BufferedReader in = new BufferedReader(new InputStreamReader(theURL
					.openStream()));
			String inputLine;
			String data = "";

			while ((inputLine = in.readLine()) != null) {
				data = data + inputLine + "\n";
			}

			in.close();
			return data;
		} catch (Throwable t) {
			throw new RuntimeException(t);
		}
	}

	public static void addPrefixes(List<List<String>> tableData, String symbol,
			String timestamp, String typeOfStatement, String periodType) {
		if (tableData.size() == 0) {
			return;
		}
		int len = tableData.get(0).size();
		List<String> newRow1 = new ArrayList<String>();
		List<String> newRow2 = new ArrayList<String>();
		List<String> newRow3 = new ArrayList<String>();
		List<String> newRow4 = new ArrayList<String>();
		List<String> newRow5 = new ArrayList<String>();
		for (int i = 0; i < len; i++) {
			if (i == 0) {
				newRow1.add("Symbol");
				newRow2.add("Timestamp");
				newRow3.add("Period");
				newRow4.add("Statement-Type");
				newRow5.add("Period-Type");
			} else {
				newRow1.add(symbol);
				newRow2.add(timestamp);
				newRow3.add("T-" + i);
				newRow4.add(typeOfStatement);
				newRow5.add(periodType);
			}
		}
		tableData.add(0, newRow5);
		tableData.add(0, newRow4);
		tableData.add(0, newRow3);
		tableData.add(0, newRow2);
		tableData.add(0, newRow1);
	}

	// For each period (e.g. year), create a separate table
	public static List<Map<String, String>> splitIntoYearly(String symbol,
			List<List<String>> tableData) {
		List<Map<String, String>> theSplitTables = new ArrayList<Map<String, String>>();
		if (tableData.size() == 0) {
			return theSplitTables;
		}
		int numPeriods = tableData.get(0).size() - 1;
		// Create an empty table for each period
		for (int k = 0; k < numPeriods; k++) {
			Map<String, String> theSplitTable = new HashMap<String, String>();
			theSplitTables.add(theSplitTable);
			// For each row of the original table
			for (int i = 0; i < tableData.size(); i++) {
				List<String> theTableRow = tableData.get(i);
				// Map<String, String> theSplitRow = new HashMap<String,
				// String>();
				// Each table contains, the first column as the name and the
				// (k+1)th element as the value
				theSplitTable.put(theTableRow.get(0), theTableRow.get(k + 1));
				// theSplitTable.add(theSplitRow);
			}
			String theStatementSourceDate = theSplitTable
					.get("Period End Date");
			String theHistoricalQuote = getHistoricalQuote(symbol,
					theStatementSourceDate);
			theSplitTable.put("Historical-Quote", theHistoricalQuote);
		}
		return theSplitTables;
	}

	/**
	 * Transpose rows/columns
	 * 
	 * @param tableData
	 * @return
	 */
	public static List<List<String>> transposeListOfLists(
			List<List<String>> tableData) {
		List<List<String>> theData = new ArrayList<List<String>>();
		if (tableData.size() == 0) {
			return theData;
		}
		int newNumberOfColumns = tableData.size();
		int newNumberOfRows = tableData.get(0).size();
		for (int i = 0; i < newNumberOfRows; i++) {
			List<String> theRow = new ArrayList<String>();
			for (int j = 0; j < newNumberOfColumns; j++) {
				theRow.add(tableData.get(j).get(i));
			}
			theData.add(theRow);
		}
		return theData;
	}

	public static void printTabSeparatedTransposed(String symbol,
			String annualOrQuarterly) throws Throwable {
		List<List<String>> theBalanceSheetData = getFinancialDataFromMoneyCentral(
				symbol, annualOrQuarterly, "Balance");
		List<List<String>> theCashFlowData = getFinancialDataFromMoneyCentral(
				symbol, annualOrQuarterly, "CashFlow");
		List<List<String>> theIncomeStatementData = getFinancialDataFromMoneyCentral(
				symbol, annualOrQuarterly, "Income");

		for (List<String> theRow : theBalanceSheetData) {
			for (String theCell : theRow) {
				System.out.print(theCell + "\t");
			}
			System.out.println("END-OF-LINE");
		}
	}

	/**
	 * 
	 * @param symbol
	 * @param annualOrQuarterly
	 * @return Returns an array containing 3 elements - 1st element contains the
	 *         balance sheet - 2nd element contains the cashflow - 3rd element
	 *         contains the income statement Each element contains (typically) 5
	 *         elements in turn - one for each period going backward
	 */
	public static JSONArray getSplitAndTaggedFinancialData(String symbol,
			String annualOrQuarterly) {
		List<List<Map<String, String>>> entireDataSet = new ArrayList<List<Map<String, String>>>();
		// Get basic table data
		List<List<String>> theBalanceSheetData = getFinancialDataFromMoneyCentral(
				symbol, annualOrQuarterly, "Balance");
		List<List<String>> theCashFlowData = getFinancialDataFromMoneyCentral(
				symbol, annualOrQuarterly, "CashFlow");
		List<List<String>> theIncomeStatementData = getFinancialDataFromMoneyCentral(
				symbol, annualOrQuarterly, "Income");
		String theTimeStamp = getGMTTimeStamp();
		// Add prefixes (tags) to the downloaded data
		addPrefixes(theBalanceSheetData, symbol, theTimeStamp, "BalanceSheet",
				annualOrQuarterly);
		addPrefixes(theCashFlowData, symbol, theTimeStamp, "CashFlow",
				annualOrQuarterly);
		addPrefixes(theIncomeStatementData, symbol, theTimeStamp, "Income",
				annualOrQuarterly);
		// Split each table into multiple tables - one for each period
		entireDataSet.add(splitIntoYearly(symbol, theBalanceSheetData));
		entireDataSet.add(splitIntoYearly(symbol, theCashFlowData));
		entireDataSet.add(splitIntoYearly(symbol, theIncomeStatementData));
		return JSONArray.fromObject(entireDataSet);
	}

	private static String getGMTTimeStamp() {
		Date theDate = new Date(System.currentTimeMillis());
		DateFormat df = new SimpleDateFormat("yyyy-MMMMM-dd HH:mm Z");
		df.setTimeZone(TimeZone.getTimeZone("GMT"));
		String theTimeStamp = df.format(theDate);
		return theTimeStamp;
	}

	public static String getHistoricalQuote(String symbol, String date) {
		try {
			// http://finance.yahoo.com/q/hp?s=GE&a=00&b=4&c=2010&d=00&e=4&f=2010&g=d
			// http://ichart.finance.yahoo.com/table.csv?s=GE&a=00&b=2&c=1962&d=04&e=2&f=2010&g=d&ignore=.csv
			Date theParsedDate = DateUtils.parseDate(date,
					new String[] { "MM/dd/yyyy" });
			Calendar theCalendar = Calendar.getInstance();
			theCalendar.setTime(theParsedDate);
			return getHistoricalQuoteDataNearDate(symbol, theCalendar);
		} catch (Throwable t) {
			throw new RuntimeException(t);
		}
	}

	private static String getHistoricalQuoteDataNearDate(String symbol,
			Calendar theCalendar) {
		for (int i = 0; i < 30; i++) {
			try {
				String theURL = String
						.format(
								"http://ichart.finance.yahoo.com/table.csv?s=%s&a=%02d&b=%d&c=%d&d=%02d&e=%d&f=%d&g=d&ignore=.csv",
								symbol, theCalendar.get(Calendar.MONTH),
								theCalendar.get(Calendar.DATE), theCalendar
										.get(Calendar.YEAR), theCalendar
										.get(Calendar.MONTH), theCalendar
										.get(Calendar.DATE), theCalendar
										.get(Calendar.YEAR));
				// System.out.println(theURL);
				theCalendar.add(Calendar.DATE, i);
				// return readDataFromURL(theURL).replace('\n', '|');
				// System.out.println(readDataFromURL(theURL));
				return readDataFromURL(theURL).split("\n")[1].split(",")[4];
			} catch (Exception ex) {
				LoggerFactory.getLogger("TEST").warn("retrying", ex);
			}
		}
		throw new RuntimeException("Could not find any data for " + symbol
				+ " around " + theCalendar);
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		JSONArray theSplitAndTaggedBalanceSheetData = getSplitAndTaggedFinancialData(
				"CSCO", "Ann");
		System.out.println(JSONArray
				.fromObject(theSplitAndTaggedBalanceSheetData));
	}
}

package net.gadgil.fundamental.screenscrape;

import java.util.ArrayList;
import java.util.List;

import com.gargoylesoftware.htmlunit.BrowserVersion;
import com.gargoylesoftware.htmlunit.Page;
import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.html.HtmlElement;
import com.gargoylesoftware.htmlunit.html.HtmlPage;

public class FundamentalScrape {

	public static List<List<String>> getFinancialDataFromMoneyCentral(
			String symbol, String annualOrQuarterly, String typeOfStatement)
			throws Throwable {
		List<List<String>> theData = new ArrayList<List<String>>();
		WebClient theWebClient = new WebClient(BrowserVersion.FIREFOX_3);
		HtmlPage thePage = theWebClient
				.getPage("http://moneycentral.msn.com/investor/invsub/results/statemnt.aspx?Symbol="
						+ symbol
						+ "&lstStatement="
						+ typeOfStatement
						+ "&stmtView=" + annualOrQuarterly);
		HtmlElement theHtmlElement = thePage.getElementById("StatementDetails");
		List<HtmlElement> theElements = theHtmlElement.getElementsByAttribute(
				"table", "class", "ftable");
		HtmlElement theTable = theElements.get(0);
		List<HtmlElement> theRows = theTable.getElementsByTagName("tr");
		for (HtmlElement theRow : theRows) {
			List<HtmlElement> theCells = theRow.getElementsByTagName("td");
			List<String> row = new ArrayList<String>();
			if (theCells.size() != 6) {
				continue;
			}
			for (HtmlElement theCell : theCells) {
				String theText = theCell.getTextContent().replaceAll(",", "")
						.trim();
				if (theText.isEmpty() || theText.length() == 1) {
					if (row.size() > 0) {
						System.err.println("Skipping data for " + row);
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
	}

	public static void printTabSeparated(List<List<String>> tableData) {
		for (List<String> theRow : tableData) {
			for (String theCell : theRow) {
				System.out.print(theCell + "\t");
			}
			System.out.println("END-OF-LINE");
		}
	}

	public static void addPrefixes(List<List<String>> tableData, String symbol, String timestamp) {
		if(tableData.size() == 0) {
			return;
		}
		int len = tableData.get(0).size();
		List<String> newRow1 = new ArrayList<String>();
		List<String> newRow2 = new ArrayList<String>();
		List<String> newRow3 = new ArrayList<String>();
		for(int i=0; i<len; i++) {
			if(i == 0) {
				newRow1.add("Symbol");
				newRow2.add("Timestamp");
				newRow3.add("Period");
			} else {
				newRow1.add(symbol);
				newRow2.add(timestamp);
				newRow3.add("T-" + i);
			}
		}
		tableData.add(0, newRow3);
		tableData.add(0, newRow2);
		tableData.add(0, newRow1);
	}
	
	public static List<List<String>> transposeListOfLists(List<List<String>> tableData) {
		List<List<String>> theData = new ArrayList<List<String>>();
		if(tableData.size() == 0) {
			return theData;
		}
		int newNumberOfColumns = tableData.size();
		int newNumberOfRows = tableData.get(0).size();
		for(int i=0; i<newNumberOfRows; i++) {
			List<String> theRow = new ArrayList<String>();
			for(int j=0; j<newNumberOfColumns; j++) {
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
	 * @param args
	 */
	public static void main(String[] args) throws Throwable {
		// TODO Auto-generated method stub
		List<List<String>> theBalanceSheetData = getFinancialDataFromMoneyCentral(
				"CVV", "Ann", "Balance");
		List<List<String>> theCashFlowData = getFinancialDataFromMoneyCentral(
				"GOOG", "Ann", "CashFlow");
		List<List<String>> theIncomeStatementData = getFinancialDataFromMoneyCentral(
				"CVV", "Ann", "Income");
		// printTabSeparated(theBalanceSheetData);
		addPrefixes(theCashFlowData, "GOOG", "4/23/2010");
		printTabSeparated(theCashFlowData);
		// printTabSeparated(theIncomeStatementData);
	}
}

package net.gadgil.fundamental.screenscrape;

import java.util.ArrayList;
import java.util.List;

import com.gargoylesoftware.htmlunit.BrowserVersion;
import com.gargoylesoftware.htmlunit.Page;
import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.html.HtmlElement;
import com.gargoylesoftware.htmlunit.html.HtmlPage;

public class FundamentalScrape {

	public static List<List<String>> getFinancialDataFromMoneyCentral(String symbol,
			String annualOrQuarterly, String typeOfStatement) throws Throwable {
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
			if(theCells.size() !=6) {
				continue;
			}
			for (HtmlElement theCell : theCells) {
				String theText = theCell.getTextContent().replaceAll(",", "").trim();
				if(theText.isEmpty() || theText.length() == 1) {
					if(row.size() > 0) {
						System.err.println("Skipping data for " + row);
					}
					continue;
				}
				//System.out.print(theText + "\t");
				//System.out.println(theText.getBytes());
				row.add(theText);
			}
			if(row.size() == 6) {
				theData.add(row);
				//System.out.println();
			}
		}
		//System.out.println(theHtmlElement);
		return theData;
	}

	public static void printTabSeparated(List<List<String>> tableData) {
		for(List<String> theRow: tableData) {
			for(String theCell: theRow) {
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
		List<List<String>> theBalanceSheetData = getFinancialDataFromMoneyCentral("C", "Ann", "Balance");
		List<List<String>> theCashFlowData = getFinancialDataFromMoneyCentral("C", "Ann", "CashFlow");
		List<List<String>> theIncomeStatementData = getFinancialDataFromMoneyCentral("C", "Ann", "Income");
		//printTabSeparated(theBalanceSheetData);
		printTabSeparated(theCashFlowData);
		//printTabSeparated(theIncomeStatementData);
	}
}

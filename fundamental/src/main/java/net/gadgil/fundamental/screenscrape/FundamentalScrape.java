package net.gadgil.fundamental.screenscrape;

import java.util.List;

import com.gargoylesoftware.htmlunit.BrowserVersion;
import com.gargoylesoftware.htmlunit.Page;
import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.html.HtmlElement;
import com.gargoylesoftware.htmlunit.html.HtmlPage;

public class FundamentalScrape {

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Throwable {
		// TODO Auto-generated method stub
		WebClient theWebClient = new WebClient(BrowserVersion.FIREFOX_3);
		HtmlPage thePage = theWebClient
				.getPage("http://moneycentral.msn.com/investor/invsub/results/statemnt.aspx?Symbol=AAPL&stmtView=Ann");
		HtmlElement theHtmlElement = thePage.getElementById("StatementDetails");
		List<HtmlElement> theElements = theHtmlElement.getElementsByAttribute("table", "class", "ftable");
		HtmlElement theTable = theElements.get(0);
		List<HtmlElement> theRows = theTable.getElementsByTagName("tr");
		for(HtmlElement theRow: theRows) {
			List<HtmlElement> theCells = theRow.getElementsByTagName("td");
			for(HtmlElement theCell: theCells) {
				System.out.print(theCell.getTextContent() + "\t");
			}
			System.out.println("");
		}
		System.out.println(theHtmlElement);
	}

}

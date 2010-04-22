package net.gadgil.fundamental.screenscrape;

import java.util.ArrayList;
import java.util.List;

import com.gargoylesoftware.htmlunit.BrowserVersion;
import com.gargoylesoftware.htmlunit.Page;
import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.html.HtmlElement;
import com.gargoylesoftware.htmlunit.html.HtmlPage;

public class FundamentalScrape {

	public static List<List<String>> getFinancialData(String symbol,
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
				String theText = trim(theCell.getTextContent().replaceAll(",", ""));
				if(theText.isEmpty()) {
					continue;
				}
				//System.out.print(theText + "\t");
				//System.out.println(theText.getBytes());
				row.add(theText);
			}
			if(row.size() == 6) {
				theData.add(row);
				System.out.println(row);
			}
		}
		System.out.println(theHtmlElement);
		return theData;

	}

    /* remove leading whitespace */
    public static String ltrim(String source) {
        return source.replaceAll("^\\s+", "");
    }

    /* remove trailing whitespace */
    public static String rtrim(String source) {
        return source.replaceAll("\\s+$", "");
    }

    /* replace multiple whitespaces between words with single blank */
    public static String itrim(String source) {
        return source.replaceAll("\\b\\s{2,}\\b", " ");
    }

    /* remove all superfluous whitespaces in source string */
    public static String trim(String source) {
        return itrim(ltrim(rtrim(source)));
    }

    public static String lrtrim(String source){
        return ltrim(rtrim(source));
    }

	
	/**
	 * @param args
	 */
	public static void main(String[] args) throws Throwable {
		// TODO Auto-generated method stub
		getFinancialData("ADCT", "Ann", "Balance");
	}

}

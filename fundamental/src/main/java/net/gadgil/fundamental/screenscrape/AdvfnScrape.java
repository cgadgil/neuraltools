package net.gadgil.fundamental.screenscrape;

import java.io.BufferedInputStream;
import java.io.ByteArrayInputStream;
import java.io.StringBufferInputStream;
import java.io.StringReader;
import java.util.List;

import javax.xml.parsers.DocumentBuilderFactory;

import org.apache.commons.io.IOUtils;
import org.apache.xmlbeans.XmlObject;
import org.w3c.dom.Document;

import com.gargoylesoftware.htmlunit.BrowserVersion;
import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.html.HtmlPage;

public class AdvfnScrape {

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Throwable {
		// TODO Auto-generated method stub
		WebClient theWebClient = new WebClient(BrowserVersion.FIREFOX_3);
		theWebClient.setJavaScriptTimeout(2000);
		theWebClient.setTimeout(5000);
		theWebClient.setJavaScriptEnabled(false);
		theWebClient.setPopupBlockerEnabled(true);
		String theSymbol = "CSCO";
		String theUrl = "http://www.advfn.com/p.php?pid=financials&symbol="
				+ theSymbol;
		HtmlPage thePage = theWebClient.getPage(theUrl);
		String xmlText = thePage.asXml();
		xmlText = xmlText.replaceAll("<?xml version=\"1.0\" encoding=\"UTF-8\"?>", "");
		DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
		//ByteArrayInputStream bais = new ByteArrayInputStream(xmlText.getBytes());
		XmlObject.Factory.parse(IOUtils.toInputStream(xmlText));
//		Document doc = dbf.newDocumentBuilder().parse(
//			IOUtils.toInputStream(xmlText));
		// doc.ge
		// List x = thePage
		// .getByXPath("//form/table/tr/td/center/table/tr/td/table/tr/td/table/tr/td[p=\"Altman's Z-Score Ratio\"]/../td[2]/p/text()");
		// List x = thePage
		// .getByXPath("//td");
		// thePage.get
		System.err.println(thePage.asXml());
	}
}

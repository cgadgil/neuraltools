/**
 * 
 */
package net.gadgil.fundamental.servlets;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.UUID;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import net.gadgil.fundamental.screenscrape.FundamentalScrape;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

/**
 * @author cgadgil
 * 
 */
public class FundamentalDataServlet extends HttpServlet {

	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp)
			throws ServletException, IOException {
		PrintWriter out = resp.getWriter();
		// out.println(req.getContextPath());
		String thePathInfo = req.getPathInfo();
		String[] theRestParams = thePathInfo.split("/");
		System.out.println(thePathInfo + theRestParams.length);
		String theSymbol = theRestParams[1];
		String thePeriodType = theRestParams[2];
		JSONArray theSplitAndTaggedBalanceSheetData = FundamentalScrape
				.getSplitAndTaggedFinancialData(theSymbol, thePeriodType);
		JSONObject theOutputObj = new JSONObject();
		theOutputObj.put("generated-id", UUID.randomUUID().toString());
		theOutputObj.put("symbol", theSymbol);
		theOutputObj.put("period-type", thePeriodType);
		theOutputObj.put("data", theSplitAndTaggedBalanceSheetData);
		// theOutputObj.put("number-of-periods",
		// theSplitAndTaggedBalanceSheetData.get(0))
		// out.println(req.getPathTranslated());
		// out.println("SimpleServlet Executed");
		out.print(theOutputObj.toString());
		out.flush();
		out.close();
	}

}

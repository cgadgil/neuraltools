/**
 * 
 */
package net.gadgil.fundamental.servlets;

import java.io.IOException;
import java.util.Arrays;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import net.sf.json.JSONArray;

import org.apache.commons.math.stat.regression.OLSMultipleLinearRegression;

/**
 * @author cgadgil
 * 
 */
public class RegressionServlet extends HttpServlet {
	
	private double[][] transpose(double[][] matrix) {
		double[][] theTranspose = new double[matrix[0].length][matrix.length];
		for(int i=0; i<matrix.length; i++) {
			for(int j=0; j<matrix[0].length; j++) {
				theTranspose[j][i] = matrix[i][j];
			}
		}
		return theTranspose;
	}

	private double[] getAsPrimitiveArray(Object[] objArray) {
		double[] theDoublePrimitiveArray = new double[objArray.length];
		for (int j = 0; j < objArray.length; j++) {
			theDoublePrimitiveArray[j] = (Double) objArray[j];
		}
		return theDoublePrimitiveArray;
	}

	/**
	 * Also supports jagged arrays
	 * 
	 * @param objArray
	 * @return
	 */
	private double[][] getAsPrimitiveArray(Object[][] objArray) {
		if (objArray.length == 0) {
			return new double[][] {};
		}
		double[][] theDoublePrimitiveArray = new double[objArray.length][objArray[0].length];
		for (int i = 0; i < objArray.length; i++) {
			theDoublePrimitiveArray[i] = this.getAsPrimitiveArray(objArray[i]);
		}
		return theDoublePrimitiveArray;
	}

	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp)
			throws ServletException, IOException {
		// TODO Auto-generated method stub
		// super.doGet(req, resp);
		String xData = req.getParameter("xData");
		String yData = req.getParameter("yData");
		if (xData == null || yData == null) {
			throw new RuntimeException("Incomplete data: xData = " + xData
					+ " yData = " + yData);
		}
		Object[][] ox = (Object[][]) JSONArray.toArray(JSONArray
				.fromObject(xData));
		Object[] oy = (Object[]) JSONArray.toArray(JSONArray.fromObject(yData));
		double[][] xDataTable = this.getAsPrimitiveArray(ox);
		double[] yDataTable = this.getAsPrimitiveArray(oy);
		System.out.println(Arrays.toString(yDataTable));
		// System.out.println(xData);
		// System.out.println(yData);
		OLSMultipleLinearRegression theOLSMLR = new OLSMultipleLinearRegression();
		theOLSMLR.newSampleData(yDataTable, xDataTable);
		System.out.println(Arrays.toString(theOLSMLR
				.estimateRegressionParameters()));
		System.out.println(theOLSMLR.estimateRegressandVariance());
		System.out.println(Arrays.toString(theOLSMLR
				.estimateRegressionParametersVariance()[0]));
		System.out.println(Arrays.toString(theOLSMLR.estimateResiduals()));
		theOLSMLR.estimateResiduals();
		resp.getOutputStream().write("OK".getBytes());
		resp.getOutputStream().close();
		// super.doGet(req, resp);
	}

	@Override
	protected void doPost(HttpServletRequest req, HttpServletResponse resp)
			throws ServletException, IOException {
		// TODO Auto-generated method stub
		// super.doPost(req, resp);
		this.doGet(req, resp);
	}

}

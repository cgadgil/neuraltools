/**
 * 
 */
package net.gadgil.analysis.regression;

import flanagan.analysis.Regression;

/**
 * @author cgadgil
 * 
 */
public class RegressionUtil {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		double[][] xdata = new double[][] { new double[] { 1, 2, 3, 4, 5 },
				new double[] { 3, 2, 4, 2, 11 }, new double[] { 4, 2, 4, 2, 1 } };
		double[] ydata = new double[] { 11, 24, 31, 42, 48 };
		double[] xd1 = new double[] { 1, 2, 3, 4, 5 };
		double[] yd1 = new double[] { 21, 32, 45, 51, 59 };
		Regression theRegression = new Regression(xdata, ydata);
		theRegression.linearGeneral();
		// theRegression.enterData(xxData, binWidth)
		// System.out.println(theRegression.getAdjustedR2());
		System.out.println(theRegression.getAdjustedR2());
		//theRegression.print("/tmp/reg.txt");
	}

}

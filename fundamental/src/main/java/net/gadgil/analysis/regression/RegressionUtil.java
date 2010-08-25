/**
 * 
 */
package net.gadgil.analysis.regression;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.apache.commons.math.stat.regression.OLSMultipleLinearRegression;

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
		double[][] xdata1 = new double[][] { new double[] { 1, 1, 2, 3 },
				new double[] { 1, 3, 2, 4 }, new double[] { 1, 4, 2, 4 },
				new double[] { 1, 6, 12, 54 }, new double[] { 1, 6, 12, 54 } };
		double[] ydata1 = new double[] { 11, 24, 31, 42, 48 };
		double[] xd1 = new double[] { 1, 2, 3, 4, 5 };
		double[] yd1 = new double[] { 21, 32, 45, 51, 59 };
		// Regression theRegression = new Regression(xdata, ydata);
		// theRegression.linearGeneral();
		// //theRegression.
		// // theRegression.enterData(xxData, binWidth)
		// // System.out.println(theRegression.getAdjustedR2());
		// System.out.println(theRegression.getAdjustedR2());
		// theRegression.print("/tmp/reg.txt");
		// theRegression.getR
		OLSMultipleLinearRegression tomlr = new OLSMultipleLinearRegression();
		tomlr.newSampleData(ydata1, xdata1);
		System.out.println(Arrays.toString(tomlr.estimateRegressionParameters()));
		//tomlr.
		System.out.println(Arrays.toString(tomlr.estimateResiduals()));
		System.out.println(tomlr.calculateRSquared());
		System.out.println(tomlr.calculateAdjustedRSquared());

	}

}

/**
 * 
 */
package net.gadgil.analysis.regression;

import javax.vecmath.GMatrix;
import javax.vecmath.GVector;

import com.gregdennis.drej.PolynomialKernel;
import com.gregdennis.drej.Regression;
import com.gregdennis.drej.Representer;

/**
 * @author cgadgil
 *
 */
public class DrejExample {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		// Initialize x values
		double[] xvalues = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

		// Initialize y values
		double[] yvalues = {1, 4, 9, 16, 25, 36, 49, 64, 81, 100};

		GMatrix data = new GMatrix(1,10,xvalues);
		GVector values = new GVector(yvalues);

		// Set up the Kernel and Solver
		// Use the pre-made PolynomialKernel kernel until the Regression works
		// Then use the custom FitKernel below
		PolynomialKernel kernel = new PolynomialKernel(3);
		double lambda = 0.5;

		// Run the Regression
		Representer representer = Regression.solve(data, values, kernel, lambda);

		// Print out the chosen "Degree"
		System.out.println("Degree: " + kernel.degree());
		System.out.println(representer.coeffs());

		// Evaluate the Regression at x = 3 - should give 9
		//double predictedValue = representer.eval(3.0);
		//System.out.println("3^2: " + predictedValue);
	}

}

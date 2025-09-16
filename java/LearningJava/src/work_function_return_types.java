public class work_function_return_types {

	public static double calculateTotalMealPrice(double listedMealPrice,
											   double tipRate,
											   double taxRate) {
		double tip = tipRate * listedMealPrice;
		double tax = taxRate * listedMealPrice;
		double result = listedMealPrice + tip + tax;
		return result;
	}
	public static void main(String[] args) {

		double groupTotalMealPrice = calculateTotalMealPrice(20, 0.1, 0.18);
		System.out.println(groupTotalMealPrice);

		double individualeMealPrice = groupTotalMealPrice / 5;
		System.out.println(individualeMealPrice);
	}
}

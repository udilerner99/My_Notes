public class work_run_triangle {

	public static void main(String[] args) {
		Triangle triangleA = new Triangle(15,15,8,17, 20);
		Triangle triangleB = new Triangle(3,2.598,3,3, 3);

		double traingleAArea = triangleA.findArea();
		System.out.println(traingleAArea);

		double traingleBArea = triangleB.findArea();
		System.out.println(traingleBArea);

		System.out.println(triangleA.base);
		System.out.println(triangleB.sideLenThree);
		System.out.println(Triangle.numOfSides);
	}
}

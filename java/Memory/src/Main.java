public class Main {

	public static void main(String[] args) {
		Customer c = new Customer("Sally");
		renameCustomer(c);
		System.out.println(c.getName());
	}

	public static void renameCustomer(Customer cust) {
		cust.setName("Diana");
	}

}

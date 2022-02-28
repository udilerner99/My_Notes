package my_package;

import java.io.IOException;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class Review {

	public static void main(String[] args) throws IOException {
		Path file = FileSystems.getDefault().getPath(System.getProperty("user.dir") + "/src/", "file.txt");
		List<String> lines = Files.readAllLines(file);
		//for (int i = 0; i < lines.size(); i++) {
		//	System.out.println(lines.get(i));
		//}
		//lines.forEach((str) ->System.out.println(str));
		lines.forEach(System.out::println);
	}

}

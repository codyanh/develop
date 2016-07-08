import java.io.IOException;
import java.net.URISyntaxException;

import org.apache.http.client.ClientProtocolException;

public class Launcher {
	public static void main(String[] args) throws ClientProtocolException,
			IOException, URISyntaxException {
		if (args[0].equals("-GET")) {
			GetExample ref = new GetExample(args[1], args[2], args[3]);
			ref.startRefresh();
		}
		if (args[0].equals("-POST")) {
			PostExample ref = new PostExample(args[1], args[2], args[3]);
			ref.startRefresh();
		}
	}
}

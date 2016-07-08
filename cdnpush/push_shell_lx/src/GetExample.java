import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.utils.URIUtils;
import org.apache.http.client.utils.URLEncodedUtils;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

/**
 * @author Archie
 */
public class GetExample {
	private final String username;
	private final String password;
	private final String rid;

	public GetExample(String username, String password, String rid) {
		super();
		this.username = username;
		this.password = password;
		this.rid = rid;
	}

	public void startRefresh() throws ClientProtocolException, IOException,
			URISyntaxException {
		HttpClient httpClient = new DefaultHttpClient();

		List<NameValuePair> qparams = new ArrayList<NameValuePair>();
		qparams.add(new BasicNameValuePair("username", username));
		qparams.add(new BasicNameValuePair("password", password));
		URI uri = URIUtils.createURI("https", "r.chinacache.com", -1,
				"/content/refresh/" + rid, URLEncodedUtils.format(qparams,
						"UTF-8"), null);
		HttpGet httpget = new HttpGet(uri);

		// System.out.println("executing request " + httpget.getURI());

		ResponseHandler<String> responseHandler = new BasicResponseHandler();
		String responseBody = httpClient.execute(httpget, responseHandler);
		System.out.println(responseBody);

		// System.out.println("----------------------------------------");

		httpClient.getConnectionManager().shutdown();
	}

	public static void main(String[] args) throws ClientProtocolException,
			IOException, URISyntaxException {
		GetExample ref = new GetExample(args[0], args[1], args[2]);
		ref.startRefresh();
	}
}

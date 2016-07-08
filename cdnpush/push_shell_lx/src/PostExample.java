import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

/**
 * @author Halley
 */
public class PostExample {
	private final String username;
	private final String password;
	private final String task;

	public PostExample(String username, String password, String task) {
		super();
		this.username = username;
		this.password = password;
		this.task = task;
	}

	public void startRefresh() throws ClientProtocolException, IOException {
		HttpClient httpClient = new DefaultHttpClient();
		HttpPost httpPost = new HttpPost(
				"https://r.chinacache.com/content/refresh");

		List<NameValuePair> formparams = new ArrayList<NameValuePair>();
		formparams.add(new BasicNameValuePair("username", username));
		formparams.add(new BasicNameValuePair("password", password));
		formparams.add(new BasicNameValuePair("task", task));
		UrlEncodedFormEntity entity = new UrlEncodedFormEntity(formparams,
				"UTF-8");

		httpPost.setEntity(entity);

		// System.out.println("executing request " + httpPost.getURI());

		ResponseHandler<String> responseHandler = new BasicResponseHandler();
		String responseBody = httpClient.execute(httpPost, responseHandler);
		System.out.println(responseBody);

		// System.out.println("----------------------------------------");

		httpClient.getConnectionManager().shutdown();
	}

	public static void main(String[] args) throws ClientProtocolException,
			IOException {
		PostExample ref = new PostExample(args[0], args[1], args[2]);
		ref.startRefresh();
	}
}

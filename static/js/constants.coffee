class window.Constants
	@site: 'https://szilardhuber.appspot.com'
	@api_url: "#{@site}/api/v1"
	@product_list_url: "#{@api_url}/Products"
	@minutes: 60 * 1000
	@login_timeout: 10 * @minutes


class Translations
	@en:			
		"app":
			"title": "shopzenion"
			"name": "shopzenion"
		"menu":
			"what_is_it": "What is it?"
			"talk_back": "Talk back"
			"blog": "Blog"
			"login": "Login"
		"heading": "<h1>What?</h1>
					<h1>One more shopping list app?</h1>
					<p>Actually, yes. But...</p><p>{{ 'app.name' | translate }} is designed to be just <b>\"twice as simple twice as amazing\"</b>.</p>
					<p>No, it is not a joke, if you know how it could be more simple or more elegant, just let us know!</p>
					<p><a class='btn btn-primary btn-large'>Learn more &raquo;</a></p>"
		"placeholder": "<h2>Heading</h2>
        			<p>Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p>
        			<p><a class=\"btn btn-default\" href=\"#\">View details &raquo;</a></p>"
		"login":
			"title": "Login"
			"close": "Close"
			"submit": "Submit"
			"form":
				"email":
					"caption": "Email: "
					"placeholder": "Enter your email address!"
				"code":
					"caption": "Code: "
					"placeholder": "Enter the code from the email!"
	@hu:
		"app":
				"title": "shopzenion"
				"name": "shopzenion"
		"menu":
				"what_is_it": "Mi ez?"
				"talk_back": "Írd meg a véleményed!"
				"blog": "Blog"
				"login": "Belépés"

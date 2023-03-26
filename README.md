<html>
<head>
	<title>Telegram Bot README</title>
</head>
<body>
	<h1>Telegram Bot README</h1>
	<p>This code implements a Telegram bot that can generate essays for users based on their specified topic and requirements. The bot can also handle payments for users to purchase more words for their essays.</p>
	<h2>Usage</h2>
	<p>To use this code, you will need to create a Telegram bot using the BotFather bot on Telegram. Once you have created your bot, obtain its API token and add it to the <code>config.py</code> file. You will also need to set up a SQLite database to store user information and their balances.</p>
	<p>To run the bot, you can use the following command:</p>
	<code>python main.py</code>
	<p>This will start the bot and it will listen for messages from users. The bot has the following commands and functionalities:</p>
	<ul>
		<li><code>/start</code> and <code>/help</code>: Sends a welcome message to the user and provides information on how to use the bot.</li>
		<li><code>/buy_words</code>: Allows the user to purchase more words for their essays using Telegram payments.</li>
		<li><code>/check_balance</code>: Shows the user their current balance in the bot.</li>
		<li><code>/generate</code>: Starts the essay generation process by asking the user for their essay topic and requirements.</li>
	</ul>
	<p>In addition to the commands, the bot also has several inline keyboards that allow the user to interact with it and navigate through its functionalities.</p>
	<h2>Dependencies</h2>
	<p>This code requires the following dependencies:</p>
	<ul>
		<li><code>aiogram</code>: Telegram bot framework for Python</li>
		<li><code>python-telegram-bot</code>: Python wrapper for the Telegram API</li>
		<li><code>pytelegrambotapi</code>: Python wrapper for the Telegram Bot API</li>
		<li><code>sqlite3</code>: SQLite database library for Python</li>
	</ul>
	<p>You can install these dependencies using pip:</p>
	<code>pip install aiogram python-telegram-bot pytelegrambotapi sqlite3</code>
	<h2>Contributions</h2>
	<p>Contributions to this code are welcome. Please submit a pull request with your changes and ensure that the code passes all tests and linting checks.</p>
</body>

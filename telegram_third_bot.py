import telebot
import yfinance as yf
import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
import pytz

bot = telebot.TeleBot("6700271123:AAEPF6CiTi_xq2Vo8cddl-xvqfCK6VsrWOY")

url = "dataset2.txt"

dataframe = pd.read_csv(url,sep = "\t")


TIMEZONE = pytz.timezone('Asia/Calcutta')


@bot.message_handler(commands = ["Greet"])
def reply(message):
    bot.reply_to(message,"Hey,How's it going!")

@bot.message_handler(commands = ["Hello","hello", "Hello"])
def send_message(message):
    bot.send_message(message.chat.id,"hello there!")

@bot.message_handler(commands = ["THANKS","Thanks", "thanks","THANK_YOU", "Thank_You", "Thank_you", "thank_you", "thank_you"])
def send_message(message):
    bot.send_message(message.chat.id,"Glad to be of use :>!")


@bot.message_handler(commands = ["question","Question", "QUESTION"])
def send_message(message):
    bot.send_message(message.chat.id,"Some of the questions you can ask me are:"
                                     "\n\n What is the capital of France?"
                                     "\n How do I reset my password?"
                                     "\n Can you recommend a good book to read?"
                                     "\n What's the weather like today?"
                                     "\n Tell me a joke."
                                     "\n How can I improve my programming skills?"
                                     "\n Where can I find a nearby restaurant?"
                                     "\n What's the latest news on technology?"
                                     "\n How do I bake a chocolate cake?"
                                     "\n What's the meaning of life?"
                                     "\nHow does photosynthesis work?"
                                     "\n What are some good workout routines?"
                                     "\n Where can I buy a new laptop?"
                                     "\n How do I create a website?"
                                     "\n What's the best way to learn a new language?"
                                     "\n How can I reduce stress?"
                                     "\n What are the benefits of meditation?"
                                     "\n Where can I go for a weekend getaway?"
                                     "\n How do I change my email settings?"
                                     "\n Tell me a fun fact."
                                     "\n What's the tallest mountain in the world?"
                                     "\n How do I apply for a job?"
                                     "\n How does a computer's CPU work?"
                                     "\n What are the symptoms of COVID-19?"
                                     "\n How can I improve my time management?"
                                     "\n What's the recipe for homemade pizza?"
                                     "\n Where can I find free online courses?"
                                     "\n What's the difference between HTTP and HTTPS?"
                                     "\n How do I invest in stocks?"
                                     "\n What's the process of making chocolate?"
                                     "\n What's the best way to study for exams?"
                                     "\n Where can I watch the latest movies online?"
                                     "\n How do I create a budget?"
                                     "\n What's the population of New York City?"
                                     "\n Tell me a riddle."
                                     "\n How do I make a resume?"
                                     "\n What are some good travel destinations?"
                                     "\nWhat's the fastest land animal?"
                                     "\nHow do I write a cover letter?"
                                     "\n What's the history of the Eiffel Tower?"
                                     "\n How do I start a small business?"
                                     "\n What's the average lifespan of a cat?"
                                     "\n Where can I find job listings?"
                                     "\n What's the distance to the Moon?"
                                     "\n How do I make a good first impression?")


@bot.message_handler(commands = ["help","Help", "HELP"])
def send_message(message):
    bot.send_message(message.chat.id,"commands to use: \n /Hello: to interact\n /Greet: to greet\n /question: to get a list of questions you can ask me from\n /help: to get help\n /start: to start using our stock predictor \n /st_listing: to get the list of listed stocks")

@bot.message_handler(commands = ["st_listing"])
def send_message(message):
    bot.send_message(message.chat.id,"Symbol-\tName"
                                     "\n AAPL       Apple Inc."
                                     "\n HES        Hess Corporation"
                                     "\n ROIV       Roivant Sciences Ltd."
                                     "\n CVX        Chevron Corporation"
                                     "\n LINK-USD        Chainlink USD"
                                     "\n NQ=F        Nasdaq 100 Dec 23"
                                     "\n PLTR       	Palantir Technologies Inc."
                                     "\n ES=F       E-Mini S&P 500 Dec 23"
                                     "\n OKTA       Okta, Inc."
                                     "\n HARP       Harpoon Therapeutics, Inc."
                                     "\n GOOG      Alphabet Inc."
                                     "\n LMDX       LumiraDx Limited"
                                     "\n YM=F       Mini Dow Jones Indus.-$5 Dec 23"
                                     "\n U      Unity Software Inc."
                                     "\n PINS       Pinterest, Inc."
                                     "\n PHG        Koninklijke Philips N.V."
                                     "\n SQQQ       ProShares UltraPro Short"
                                     "\n QQQ        TGH	Textainer Group Holdings Limited"
                                     "\n META       Meta Platforms, Inc."
                                     "\n NIO        NIO Inc."
                                     "\n MSFT       Microsoft Corporation"
                                     "\n DOGE-USD       Dogecoin USD"
                                     "\n WTER       The Alkaline Water Company Inc."
                                     "\n AMZN       Amazon.com, Inc."
                                     "\n NVDA       NVIDIA Corporation"
                                     "\n SPY        SPDR S&P 500 ETF Trust"
                                     "\n VOW3.DE        Volkswagen AG"
                                     "\n TRKA       Troika Media Group, Inc."
                                     "\n IMMP       Immutep Limited\n")


#starting the stock perdiction
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Welcome to the Bot! Type a Stock to get prediction.")

    # Handler to respond to text messages
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        if len(message.text) <=8:
            try:
                stock_symbol = message.text
                prediction = predict_stock_price(stock_symbol)

                bot.send_message(message.chat.id, f"Predicted stock price for {stock_symbol}: {prediction:.2f}")
            except Exception as e:
                #bot.send_message(message.chat.id, "No price data found, item maybe delisted!!")
                pass
        else:
          msg = message.text
          answer = dataframe.loc[dataframe["Question"].str.lower() == msg.lower()]
          if not answer.empty:
              answer = answer.iloc[0]['Answer']
              bot.reply_to(message,answer)
          else:
            pass

    #stock predction function
    def predict_stock_price(stock_symbol):

        end_date = pd.to_datetime(datetime.datetime.now(TIMEZONE).date())
        start_date = pd.to_datetime(end_date - datetime.timedelta(days=365))

        df = yf.download(stock_symbol, start=start_date, end=end_date)


        df['Date'] = pd.to_datetime(df.index)

        day_diffs = []
        for date in df['Date']:
            days = (date - start_date).days
            day_diffs.append(days)
        df['Days'] = day_diffs
        X = df[['Days']].values
        y = df['Close'].values

        model = LinearRegression()
        model.fit(X, y)

        next_day = (end_date - start_date).days + 1
        predicted_price = model.predict([[next_day]])

        return predicted_price[0]



bot.polling()
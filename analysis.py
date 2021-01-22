import re
import string
import statistics
import pandas as pd
import nltk
from nltk import word_tokenize, sent_tokenize, pos_tag
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.ticker import FixedLocator, FixedFormatter

def add_attr(msg):
  if not 'media_type' in msg:
    msg['media_type'] = '-'
  if not 'reply_to_message_id' in msg:
    msg['reply_to_message_id'] = '-'
  return msg

def read_file(data):
  df = pd.read_json(data)
  messages = list(df.messages)
  expanded_messages = list(map(add_attr, messages)) #add media type and reply id
  cols = list(expanded_messages[0].keys())
  msg_df = pd.DataFrame(messages, columns=cols)
  msg_subset = msg_df[['id', 'date', 'from', 'text', 'media_type', 'reply_to_message_id']]
  return msg_subset

def print_nof_msg(u1_messages, u2_messages):
  nof_u1 = u1_messages.shape[0]
  nof_u2 = u2_messages.shape[0]
  total = nof_u1 + nof_u2

  print('Nof messages:')
  print('User1:', nof_u1)
  print('User2:', nof_u2)
  print('Total:', total, '\n')

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
                           
    return emoji_pattern.sub(r'', string)

def clean(message):
  msg = ''
  for part in message:
    if(isinstance(part, str)):
      msg = msg + part
    else:
      msg = msg + part['text'] 
  return msg

#make list messages (msg that contains link, bold etc.) string format
def clean_text(messages):
  text = messages.text
  clean_text = list(filter(lambda x: isinstance(x, str), text))
  dirty_text = list(filter(lambda x: not isinstance(x, str), text))
  clean_text = clean_text + list(map(clean, dirty_text))
  return clean_text

def get_nof_words(messages):
  text = clean_text(messages)
  text_string = ' '.join(text)
  nof_words = len(list(filter(None, remove_emoji(text_string).split(' '))))
  return nof_words

def print_nof_words(messages_u1, messages_u2):
  nof_u1 = get_nof_words(messages_u1)
  nof_u2 = get_nof_words(messages_u2)
  total = nof_u1 + nof_u2

  print('Nof words:')
  print('User1:', nof_u1)
  print('User2:', nof_u2)
  print('Total:', total, '\n')

def get_avg_msg_length(messages):
  clean = clean_text(messages)
  emojis_removed = list(map(lambda x: remove_emoji(x), clean)) #still has lingering spaces
  without_emoji = list(map(lambda x: ' '.join(list(filter(None, x.split(' ')))), emojis_removed))

  msg_lengths = list(map(lambda x: len(x.split(' ')), without_emoji))
  msg_lengths_emoji = list(map(lambda x: len(x.split(' ')), clean))
  avg_length = statistics.mean(msg_lengths)
  avg_length_emoji = statistics.mean(msg_lengths_emoji)

  return(avg_length, avg_length_emoji)

def print_avg_msg_length(u1_msg, u2_msg):
  avg_u1, avg_u1_emoji = get_avg_msg_length(u1_msg)
  avg_u2, avg_u2_emoji = get_avg_msg_length(u2_msg)

  print('Avg message length no emoji / with emoji:')
  print('User1:', avg_u1, ' / ', avg_u1_emoji)
  print('User2', avg_u2, ' / ', avg_u2_emoji)

# for some reason skips some emoji but good enough for now
def get_nof_emoji(messages):
  clean_messages = clean_text(messages)
  text_messages = ' '.join(clean_messages)
  nof_emoji = len(re.findall(u'[\U0001f600-\U0001F64F]', text_messages))
  return nof_emoji

def print_nof_emoji(u1_messages, u2_messages):
  nof_u1 = get_nof_emoji(u1_messages)
  nof_u2 = get_nof_emoji(u2_messages)
  total = nof_u1 + nof_u2

  print('Nof emoji:')
  print('User1:', nof_u1)
  print('User2:', nof_u2)
  print('Total:', total, '\n')

def get_nof_stickers(messages):
  medias = messages.media_type
  stickers = list(filter(lambda x: x == 'sticker', medias))
  nof_stickers = len(stickers)
  return nof_stickers

def print_nof_stickers(u1_messages, u2_messages):
  nof_u1 = get_nof_stickers(u1_messages)
  nof_u2 = get_nof_stickers(u2_messages)
  total = nof_u1 + nof_u2

  print('Nof stickers:')
  print('User1:', nof_u1)
  print('User2:', nof_u2)
  print('Total:', total, '\n')

def get_most_common_words(messages):
  clean_messages = clean_text(messages)
  text = ' '.join(list(clean_messages))
  lof_words = word_tokenize(text)

  punctuation = string.punctuation + '..' + '-' + ', ' + '' + '”'
  without_punctuation = list(filter(lambda x: x not in punctuation, lof_words))

  word_df = pd.DataFrame(without_punctuation, columns=['word'])
  word_freq_df = word_df.groupby('word').size().reset_index(name='occurences').sort_values(by=['occurences'], ascending=False).reset_index(drop=True)

  return word_freq_df.head(30)

def print_most_common_words(messages, u1_messages, u2_messages):
  u1_words = get_most_common_words(u1_messages)
  u2_words = get_most_common_words(u2_messages)
  tot_words = get_most_common_words(messages)

  print('Most common words:')
  print('Total:\n', tot_words)
  print('User1:\n', u1_words)
  print('User2:\n', u2_words)

def get_most_common_emoji(messages):
  clean_messages = clean_text(messages)
  text_messages = ' '.join(clean_messages)
  emoji = re.findall(u'[\U0001f600-\U0001F64F]', text_messages)
  emoji_df = pd.DataFrame(emoji, columns=['emoji'])
  emoji_freq_df = emoji_df.groupby('emoji').size().reset_index(name='occurences').sort_values(by=['occurences'], ascending=False)
  return emoji_freq_df.head(30)

def print_most_common_emoji(messages, u1_messages, u2_messages):
  u1_emoji = get_most_common_emoji(u1_messages)
  u2_emoji = get_most_common_emoji(u2_messages)
  tot_emoji = get_most_common_emoji(messages)
  
  print('Most common emoji:')
  print('Total:\n', tot_emoji)
  print('User1:\n', u1_emoji)
  print('User2:\n', u2_emoji)

def get_datetime_dataframe(messages):
  datetimes = list(messages.date)
  dates = list(map(lambda datetime: datetime.split('T')[0], datetimes))
  times = list(map(lambda datetime: datetime.split('T')[1], datetimes))
  hours = list(map(lambda datetime: datetime.split(':')[0], times))
  dates_df = pd.DataFrame(datetimes, columns=['datetime'])
  dates_df['date'] = dates
  dates_df['time'] = times
  dates_df['hour'] = hours
  return dates_df

def get_daily_messages(messages):
  date_df = get_datetime_dataframe(messages)
  daily_messages_df = date_df.groupby(['date']).size().reset_index(name='nof_messages')
  return daily_messages_df  

def draw_daily_messages(u1_messages, u2_messages):
  date_df_u1 = get_daily_messages(u1_messages)
  date_df_u2 = get_daily_messages(u2_messages)
  daily_messages_df = pd.DataFrame(date_df_u1, columns=['date', 'nof_messages'])
  daily_messages_df['u2_messages'] = date_df_u2['nof_messages']
  daily_messages_df.columns = ['date', 'u1_messages', 'u2_messages']
  daily_messages_df['total_messages'] = daily_messages_df['u1_messages'] + daily_messages_df['u2_messages']
  daily_messages_df['date'] = pd.to_datetime(daily_messages_df['date'])

  dates = pd.date_range(start=daily_messages_df.date.min(), end=daily_messages_df.date.max())
  daily_messages_df.set_index('date', inplace=True)
  daily_messages_df = daily_messages_df.reindex(dates, fill_value=0)
  daily_messages_df['date'] = daily_messages_df.index
  
  row_count = daily_messages_df.shape[0]
  first_date = str(daily_messages_df['date'].head(1)[0].date())
  last_date = str(daily_messages_df['date'].tail(1)[0].date())

  sns.set(rc={'axes.facecolor': '#24252A', 'figure.facecolor': '#24252A', 'axes.labelcolor': 'white', 'xtick.color': 'white', 'ytick.color': 'white', 'font.sans-serif': 'AppleGothic'})
  fig = plt.figure(figsize=(15,3))
  ax = fig.add_subplot(111)
  date = daily_messages_df['date']

  #the bar plots will not be visible with larger datasets, so in those cases show a line plot instead
  if (row_count < 700):
    plot = sns.barplot(x = date, y = daily_messages_df['total_messages'], color = '#E497AE', edgecolor='#24252A')
    bottom_plot = sns.barplot(x= date, y=daily_messages_df['u2_messages'], color='#4DABDE', edgecolor='#24252A')
  else:
    trend_plot = sns.lineplot(data=daily_messages_df['total_messages'], color='#F2A96C', linewidth=0.5)

  ax.grid(False)
  ax.spines['left'].set_linewidth(0.5)
  ax.spines['bottom'].set_linewidth(0.5)
  ax.spines['top'].set_linewidth(0)
  ax.spines['right'].set_linewidth(0)
  ax.set(xlabel=None, ylabel=None, xticks=[]) #hides labels and xticks
  ax.tick_params(labelsize=8)
  ax.axes.set_title('Daily distribution ' + first_date + ' - ' + last_date, color='white', y=1, x=0.2, fontsize=14)
  plt.legend([],[], frameon=False)

  plt.setp(ax.get_xticklabels(), rotation=30, ha='right')

  # this spaghetti was only useful for one very specific case but it's left here as a memory
  #months = FixedFormatter(['11/19', '12/19', '1/20', '2/20', '3/20', '4/20', '5/20', '6/20', '7/20', '8/20', '9/20', '10/20', '11/20'])
  #month_locs = FixedLocator([0, 19, 50, 81, 110, 141, 171, 202, 232, 263, 294, 324, 355])
  #ax.xaxis.set_major_formatter(months)
  #ax.xaxis.set_major_locator(month_locs)

  plt.show()

def get_hourly_messages(messages):
  date_df = get_datetime_dataframe(messages)
  date_df['from'] = messages['from']
  hourly_messages_df = date_df.groupby(['hour', 'from']).size().reset_index(name='nof_messages')
  total_messages = hourly_messages_df['nof_messages'].sum()
  hourly_messages_df['percents'] = hourly_messages_df['nof_messages'] / total_messages

  return hourly_messages_df

def draw_hourly_messages(messages):
  hourly_df = get_hourly_messages(messages)

  sns.set(rc={'axes.facecolor': '#24252A', 'figure.facecolor': '#24252A', 'axes.labelcolor': 'white', 'xtick.color': 'white', 'ytick.color': 'white', 'font.sans-serif': 'AppleGothic'})
  fig = plt.figure(figsize=(10,4))
  ax = sns.barplot(x ='hour', y ='nof_messages', hue ='from', data = hourly_df, palette=['#E497AE', '#4DABDE'], edgecolor='#24252A')
  ax.grid(False)
  ax.spines['left'].set_linewidth(0.5)
  ax.spines['bottom'].set_linewidth(0.5)
  ax.spines['top'].set_linewidth(0)
  ax.spines['right'].set_linewidth(0)
  ax.set(xlabel=None, ylabel=None)
  ax.tick_params(labelsize=8)
  ax.axes.set_title('Hourly distribution', color='white', y=1, x=0.0, fontsize=14)
  plt.legend([],[], frameon=False)

  plt.show()

def draw_donut_distribution(nof_u1, nof_u2, title):
  sns.set(rc={'figure.facecolor': '#24252A', 'text.color': 'white', 'font.sans-serif': 'AppleGothic'})

  plt.pie([nof_u1, nof_u2], colors=['#E497AE', '#4DABDE'], autopct='%.1f', pctdistance=0.8, startangle=90)
  empty_inside = plt.Circle((0,0), 0.6, color='#24252A', ec='white')
  p=plt.gcf()
  p.gca().add_artist(empty_inside)
  plt.title(title, y=0.45)

  plt.show()

def draw_message_length(avg_u1, avg_u2, avg_u1_emoji, avg_u2_emoji, title):
  msg_data = [['User1', avg_u1, avg_u1_emoji], ['User2', avg_u2, avg_u2_emoji]]
  avg_df = pd.DataFrame(msg_data, columns = ['Name', 'AvgLength', 'WithEmoji'])

  colors=['#E497AE','#4DABDE']
  sns.set(rc={'axes.facecolor': '#24252A', 'figure.facecolor': '#24252A', 'axes.labelcolor': 'white', 'xtick.color': 'white', 'ytick.color': 'white'})

  ax = avg_df.plot(kind='bar', x='Name', figsize=(3,6), width=0.5, legend=False, color=colors, edgecolor = '#24252A', rot=0)
  ax.grid(False)
  ax.spines['left'].set_linewidth(0.5)
  ax.spines['bottom'].set_linewidth(0.5)
  ax.spines['top'].set_linewidth(0)
  ax.spines['right'].set_linewidth(0)
  ax.set_xlabel('')
  ax.tick_params(axis='y', labelsize=8)
  ax.tick_params(axis='x', labelsize=10)
  ax.axes.set_title(title, color='white', y=1.05, fontsize=10)
  ax.legend(['No emoji', 'Yes emoji'])
  legend = plt.legend(['No emoji', 'Yes emoji'], bbox_to_anchor=(0.5, -0.05), prop={'size': 8})
  legend.get_frame().set_linewidth(0)
  plt.setp(legend.get_texts(), color='w')


  font = 'AppleGothic'
  matplotlib.rcParams['font.sans-serif'] = font

  for p in ax.patches:
    ax.annotate('{:.2f}'.format(p.get_height()), (p.get_x(), p.get_height() * 1.01), color='white', fontsize=8)

  plt.show()


def draw_emoji_barplot(msg, color):
  emoji = get_most_common_emoji(msg)
  nof_u1 = get_nof_emoji(msg)
  nof_other = nof_u1 - sum(emoji['occurences'])

  other_emoji = {'emoji': ['other'], 'occurences': [nof_other] }
  other_emoji_df = pd.DataFrame(other_emoji, columns=['emoji', 'occurences'])
  emoji_df = emoji.append(other_emoji_df)

  sns.set(rc={'axes.facecolor': '#24252A', 'figure.facecolor': '#24252A', 'axes.labelcolor': 'white', 'xtick.color': 'white', 'ytick.color': 'white'})
  ax = emoji_df.plot(kind='barh', figsize=(3,6), x='emoji', y='occurences', width=0.5, legend=False, color=color, edgecolor = 'none', rot=0)
  ax.grid(False)
  ax.spines['left'].set_linewidth(0.5)
  ax.spines['bottom'].set_linewidth(0.5)
  ax.spines['top'].set_linewidth(0)
  ax.spines['right'].set_linewidth(0)
  ax.set_xlabel('')
  ax.set_ylabel('')
  ax.set(yticklabels=[])
  ax.tick_params(axis='x', labelsize=10)
  plt.gca().invert_yaxis()

  font = 'AppleGothic'
  matplotlib.rcParams['font.sans-serif'] = font

  for p in ax.patches:
    width = p.get_width()
    plt.text(50+p.get_width(), p.get_y()+0.55*p.get_height(),
             '{:1.0f}'.format(width),
              va='center', color='white', fontsize=8)
  
  plt.show()

def run():
  is_running = True
  filename = str(input('Please give the data location: '))
  user1 = str(input('Please give the name of User 1: '))

  messages = read_file(filename)

  u1_messages = messages.loc[messages['from'] == user1 ]
  u2_messages = messages.loc[messages['from'] != user1 ]

  #nof messages
  msg_u1 = u1_messages.shape[0]
  msg_u2 = u2_messages.shape[0]

  #nof_words
  words_u1 = get_nof_words(u1_messages)
  words_u2 = get_nof_words(u2_messages)

  #nof_emoji
  emoji_u1 = get_nof_emoji(u1_messages)
  emoji_u2 = get_nof_emoji(u2_messages)

  #nof_stickers
  stickers_u1 = get_nof_stickers(u1_messages)
  stickers_u2 = get_nof_stickers(u2_messages)

  #avg message length
  avg_u1, avg_u1_emoji = get_avg_msg_length(u1_messages)
  avg_u2, avg_u2_emoji = get_avg_msg_length(u2_messages)

  # print_nof_msg(u1_messages, u2_messages)
  # print_nof_emoji(u1_messages, u2_messages)
  # print_avg_msg_length(u1_messages, u2_messages)
  # print_nof_emoji(u1_messages, u2_messages)
  # print_nof_stickers(u1_messages, u2_messages)
  # print_most_common_words(messages, u1_messages, u2_messages)
  # print_most_common_emoji(messages, u1_messages, u2_messages)
  # draw_daily_messages(u1_messages, u2_messages) #the bar plots will not be visible with larger datasets
  # draw_hourly_messages(messages)
  # draw_donut_distribution(msg_u1, msg_u2, 'Sent messages')
  # draw_donut_distribution(words_u1, words_u2, 'Number of\nwords')
  # draw_donut_distribution(emoji_u1, emoji_u2, 'Number of\nemoji')
  # draw_donut_distribution(stickers_u1, stickers_u2, 'Sent stickers')
  # draw_message_length(avg_u1, avg_u2, avg_u1_emoji, avg_u2_emoji, 'Average message length')
  # draw_emoji_barplot(u1_messages, '#E497AE')
  # draw_emoji_barplot(u2_messages, '#4DABDE')

run()
  
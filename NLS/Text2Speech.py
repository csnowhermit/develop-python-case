import pyttsx3
engine = pyttsx3.init()
# engine.say('Hello, good morning')
text = '北京天气：晴，20～33摄氏度，西北风3-4级'

# text = "" """
#     I have a dream that one day this nation will rise up and live out the true meaning of its creed: "We hold these truths to be self-evident, that all men are created equal."
# I have a dream that one day on the red hills of Georgia, the sons of former slaves and the sons of former slave owners will be able to sit down together at the table of brotherhood.
# I have a dream that one day even the state of Mississippi, a state sweltering with the heat of injustice, sweltering with the heat of oppression, will be transformed into an oasis of freedom and justice.
# I have a dream that my four little children will one day live in a nation where they will not be judged by the color of their skin but by the content of their character.
# I have a dream today!
# I have a dream that one day, down in Alabama, with its vicious racists, with its governor having his lips dripping with the words of "interposition" and "nullification" -- one day right there in Alabama little black boys and black girls will be able to join hands with little white boys and white girls as sisters and brothers.
# I have a dream today!
# I have a dream that one day every valley shall be exalted, and every hill and mountain shall be made low, the rough places will be made plain, and the crooked places will be made straight; "and the glory of the Lord shall be revealed and all flesh shall see it together."
# This is our hope, and this is the faith that I go back to the South with.
# With this faith, we will be able to hew out of the mountain of despair a stone of hope. With this faith, we will be able to transform the jangling discords of our nation into a beautiful symphony of brotherhood. With this faith, we will be able to work together, to pray together, to struggle together, to go to jail together, to stand up for freedom together, knowing that we will be free one day.
# And this will be the day -- this will be the day when all of God's children will be able to sing with new meaning:
# My country 'tis of thee, sweet land of liberty, of thee I sing.
# Land where my fathers died, land of the Pilgrim's pride,
# From every mountainside, let freedom ring!
# And if America is to be a great nation, this must become true.
# And so let freedom ring from the prodigious hilltops of New Hampshire.
# Let freedom ring from the mighty mountains of New York.
# Let freedom ring from the heightening Alleghenies of
# Pennsylvania.
# Let freedom ring from the snow-capped Rockies of Colorado.
# Let freedom ring from the curvaceous slopes of California.
# But not only that:
# Let freedom ring from Stone Mountain of Georgia.
# Let freedom ring from Lookout Mountain of Tennessee.
# Let freedom ring from every hill and molehill of Mississippi.
# From every mountainside, let freedom ring.
# And when this happens, when we allow freedom ring, when we let it ring from every village and every hamlet, from every state and every city, we will be able to speed up that day when all of God's children, black men and white men, Jews and Gentiles, Protestants and Catholics, will be able to join hands and sing in the words of the old Negro spiritual:
# Free at last! Free at last!
# Thank God Almighty, we are free at last!
# """

# text = "" """
#     我梦想有一天，这个国家会站立起来，真正实现其信条的真谛：“我们认为这些真理是不言而喻的——人人生而平等。”
# 　　我梦想有一天，在佐治亚的红山上，昔日奴隶的儿子将能够和昔日奴隶主的儿子坐在一起，共叙兄弟情谊。
# 　　我梦想有一天，甚至连密西西比州这个正义匿迹，压迫成风的地方，也将变成自由和正义的绿洲。
# 　　我梦想有一天，我的四个孩子将在一个不是以他们的肤色，而是以他们的品格优劣来评价他们的国度里生活。
# 　　我今天有一个梦想。
# 　　我梦想有一天，亚拉巴马州能够有所转变，尽管该州州长现在仍然满口异议，反对联邦法令，但有朝一日，那里的黑人男孩和女孩将能与白人男孩和女孩情同骨肉，携手并进。
# 　　我今天有一个梦想。
# 　　我梦想有一天，幽谷上升，高山下降，坎坷曲折之路成坦途，圣光披露，满照人间。
# 　　这就是我们的希望。我怀着这种信念回到南方。有了这个信念，我们将能从绝望之嶙劈出一块希望之石。有了这个信念，我们将能把这个国家刺耳争吵的声，改变成为一支洋溢手足之情的优美交响曲。
# 　　有了这个信念，我们将能一起工作，一起祈祷，一起斗争，一起坐牢，一起维护自由；因为我们知道，终有一天，我们是会自由的。
# 　　在自由到来的那一天，上帝的所有儿女们将以新的含义高唱这支歌：“我的祖国，美丽的自由之乡，我为您歌唱。您是父辈逝去的地方，您是最初移民的骄傲，让自由之声响彻每个山冈。”
# 　　如果美国要成为一个伟大的国家，这个梦想必须实现。让自由之声从新罕布什尔州的巍峨峰巅响起来！让自由之声从纽约州的崇山峻岭响起来！让自由之声从宾夕法尼亚州阿勒格尼山的顶峰响起来！
# """

# voices = engine.getProperty('voices')
# for voice in voices:
#   engine.setProperty('voice', voice.id)
#   print(voice.id)
#   engine.say(text)

engine.say(text)    # 正常语速

print(engine.getProperty("rate"))
engine.setProperty('rate', engine.getProperty("rate") - 60)    # 改变语速
# engine.setProperty('age', 18)    # 18岁
# engine.setProperty('gender', 'female')    #
engine.say(text)

print(engine.getProperty('volume'))
engine.setProperty('volume', engine.getProperty('volume') - 0.5)    # 音量
engine.say(text)


engine.runAndWait()
#!/usr/bin/env python
# coding: utf-8
#cleaner function 0.1.4


# importing all the important libraries
import re
import json
import html
import unicodedata
import pkg_resources
from ftfy import fix_text


# In[4]:


#  Cleaning raw HTML and retaining tags
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def replace_all1(text, dic):
    for i, j in dic.items():
        text = text.replace(j, i)
    return text

def cleaner(text):

    # tags = {'<p>' : '{p}', '</p>':'{/p}','<span>': '{span}','</span>':'{/span}', '<br>':'{br}','</br>':'{/br}','<b>':'{b}',
    #         '</b>':'{/b}','<i>':'{i}','</i>':'{/i}','<u>':'{u}','</u>':'{/u}' ,'<strong>':'{strong}','</strong>':'{/strong}' ,
    #         '<h1>':'{h1}','</h1>':'{/h1}','<h2>':'{h2}','</h2>':'{/h2}','<h3>':'{h3}','</h3>':'{/h3}','<h4>':'{h4}',
    #         '</h4>':'{/h4}','<h5>':'{h5}','</h5>':'{/h5}','<h6>':'{h6}','</h6>':'{/h6}', '<li>':'{li}','</li>':'{/li}',
    #         '<ol>':'{ol}', '</ol>':'{/ol}', '<img':'{img', '}>':'}}'}

    tags = {'<p>' : '{p}', '</p>':'{/p}','<span>': '{span}','</span>':'{/span}', '<br>':'{br}','</br>':'{/br}','<b>':'{b}',
            '</b>':'{/b}','<i>':'{i}','</i>':'{/i}','<u>':'{u}','</u>':'{/u}' ,'<strong>':'{strong}','</strong>':'{/strong}' ,
            '<h1>':'{h1}','</h1>':'{/h1}','<h2>':'{h2}','</h2>':'{/h2}','<h3>':'{h3}','</h3>':'{/h3}','<h4>':'{h4}',
            '</h4>':'{/h4}','<h5>':'{h5}','</h5>':'{/h5}','<h6>':'{h6}','</h6>':'{/h6}', '<li>':'{li}','</li>':'{/li}',
            '<ol>':'{ol}', '</ol>':'{/ol}',
            '<img':'{img',
            '<blockquote': '{blockquote',
            '<iframe': '{iframe',
            '<video': '{video',
            '}>':'}}',
            '</video>': '{/video}'}



    # change a tags name inside blockquote
    # clean_text = re.sub(r'<blockquote class="twitter-tweet".*?<a href="(?:https://twitter.com|TWEET_(\d+)).*?</a>.*?</blockquote>', lambda x: x.group(0).replace("<", "{").replace("}", "}"), text, flags=re.DOTALL)
    # change iframe tag name
    # clean_text = re.sub(r'<iframe.*?src="(?:https://www.youtube-nocookie.com|https://www.youtube.com).*?</iframe>', lambda x: x.group(0).replace("<", "{").replace(">", "}"), clean_text, flags=re.DOTALL)
    # display(clean_text)

    blockquote_list = re.findall(r'<blockquote class="twitter-tweet".*?<a href="(?:https://twitter.com|TWEET).*?</a>.*?</blockquote>', text, flags=re.DOTALL)
    iframe_list = re.findall(r'<iframe.*?src="(?:https://www.youtube-nocookie.com|https://www.youtube.com|YOUTUBE).*?</iframe>', text, flags=re.DOTALL)

    clean_text = re.sub(r'<blockquote class="twitter-tweet".*?<a href="(?:https://twitter.com|TWEET).*?</a>.*?</blockquote>', "<blockquote_holder>", text, flags=re.DOTALL)
    clean_text = re.sub(r'<iframe.*?src="(?:https://www.youtube-nocookie.com|https://www.youtube.com|YOUTUBE).*?</iframe>', "<iframe_holder>", clean_text, flags=re.DOTALL)





    clean_text = re.sub("""(<img)+[a-zA-Z\d\s=":/.?\-;&,_{}!–@#“”$%^*()_+=\[\]|\\'~`‘’]+(>)""", "<img_tags_retained>", clean_text)

    clean_text = re.sub("""(<img_tags_retained>[Õa-zA-ZI=".\s\d&“”#-;{},:_'?|–@#!~`$’%^&*()\-_=+\[\]]*<)""",'<img_tags_retained><',clean_text) #removing image caption
    clean_text = re.sub("""(<img_tags_retained>[Õa-zA-ZI=".\s\d&“”#-;,:_'?|–@#!~`$’%^&*()\-_=+\[\]]*<\/p>[\s]*[a-zA-Z/:]*[\s]*[a-zA-Z/:]*[\s]*[a-zA-Z/:]*[\s]*<)""",'<img_tags_retained><',clean_text) #removing image caption
    clean_text = re.sub("""(</strong>[\s]*<strong>)""",'',clean_text) #removing consecutive strong-tags


    clean_text = re.sub("""(<video)+[a-zA-Z\d\s=":/.?\-;&,_{}!–@#“”$%^*()_+=\[\]|\\'~`‘’]+(>)""", "<video_tags_retained>", clean_text)
    clean_text = re.sub("""(<video_tags_retained>[Õa-zA-ZI=".\s\d&“”#-;{},:_'?|–@#!~`$’%^&*()\-_=+\[\]]*<)""",'<video_tags_retained><',clean_text) #removing video caption
    clean_text = re.sub("""(<video_tags_retained>[Õa-zA-ZI=".\s\d&“”#-;,:_'?|–@#!~`$’%^&*()\-_=+\[\]]*<\/p>[\s]*[a-zA-Z/:]*[\s]*[a-zA-Z/:]*[\s]*[a-zA-Z/:]*[\s]*<)""",'<video_tags_retained><',clean_text) #removing video caption
    clean_text = re.sub("""(</strong>[\s]*<strong>)""",'',clean_text) #removing consecutive strong-tags


    # clean_text = re.sub("""(<iframe)+[a-zA-Z\d\s=":/.?\-;&,_{}!–@#“”$%^*()_+=\[\]|\\'~`‘’]+(>)""", "<iframe_tags_retained>", clean_text)
    # clean_text = re.sub("""(<iframe_tags_retained>[Õa-zA-ZI=".\s\d&“”#-;{},:_'?|–@#!~`$’%^&*()\-_=+\[\]]*<)""",'<iframe_tags_retained><',clean_text) #removing iframe caption
    # clean_text = re.sub("""(<iframe_tags_retained>[Õa-zA-ZI=".\s\d&“”#-;,:_'?|–@#!~`$’%^&*()\-_=+\[\]]*<\/p>[\s]*[a-zA-Z/:]*[\s]*[a-zA-Z/:]*[\s]*[a-zA-Z/:]*[\s]*<)""",'<iframe_tags_retained><',clean_text) #removing iframe caption
    # clean_text = re.sub("""(</strong>[\s]*<strong>)""",'',clean_text) #removing consecutive strong-tags


    if "<img_tags_retained>" in clean_text:
        img_tags = clean_text.split("<img_tags_retained>")
        img_tag_list = []
        stop = len(img_tags)-1
        for ind,i in enumerate(img_tags):
            img_tag_list.append(i)
            if ind != stop:
                img_tag_list.append("{img src={IMG_" + str(ind) + "}>")

        clean_text = "".join(img_tag_list)


    if "<video_tags_retained>" in clean_text:
        vid_tags = clean_text.split("<video_tags_retained>")
        vid_tag_list = []
        stop = len(vid_tags)-1
        for ind,i in enumerate(vid_tags):
            vid_tag_list.append(i)
            if ind != stop:
                vid_tag_list.append("{video src={VIDEO_" + str(ind) + "}>")

        clean_text = "".join(vid_tag_list)

    if "<blockquote_holder>" in clean_text:
        block_tags = clean_text.split("<blockquote_holder>")
        block_tag_list = []
        stop = len(block_tags)-1
        for ind,i in enumerate(block_tags):
            block_tag_list.append(i)
            if ind != stop:
                block_tag_list.append("{blockquote src={BLOCK_" + str(ind) + "}>")

        clean_text = "".join(block_tag_list)

    if "<iframe_holder>" in clean_text:
        iframe_tags = clean_text.split("<iframe_holder>")
        iframe_tag_list = []
        stop = len(iframe_tags)-1
        for ind,i in enumerate(iframe_tags):
            iframe_tag_list.append(i)
            if ind != stop:
                iframe_tag_list.append("{iframe src={IFRAME_" + str(ind) + "}>")

        clean_text = "".join(iframe_tag_list)




    # if "<iframe_tags_retained>" in clean_text:
    #     iframe_tags = clean_text.split("<iframe_tags_retained>")
    #     iframe_tag_list = []
    #     stop = len(iframe_tags)-1
    #     for ind,i in enumerate(iframe_tags):
    #         iframe_tag_list.append(i)
    #         if ind != stop:
    #             iframe_tag_list.append("{iframe src={YOUTUBE_" + str(ind) + "}>")

    #     clean_text = "".join(iframe_tag_list)

    clean_text = replace_all(clean_text, tags)
    # display(clean_text)


    clean_text = re.sub(r'<[^<>]*>', ' ',clean_text) #removing all html tags
    # display(clean_text)
    clean_text = re.sub('http[s]?://\S+', ' ', clean_text) # removing all urls
    # display(clean_text)
    clean_text = re.sub('\S*@\S*\s?', '',clean_text) #removing all links
    clean_text = re.sub('\|*Advertisement\|*','',clean_text) #removing Advertisement keyword
    clean_text = re.sub('\|*(Getty Images)\|*','',clean_text) #removing getty images keyword
    # display(clean_text)


    # Removing Pattern from independent.uk.co
    clean_text = re.sub(".*" + "r {{ /verifyErrors }}", '', clean_text)
    clean_text = re.sub(".*" + "Washington email" , '', clean_text)
    clean_text = re.sub(".*" + "breaking news emails", '', clean_text)
    clean_text = re.sub(".*" + "for all the latest news", '', clean_text)
    clean_text = re.sub(".*" + "This email for free", '', clean_text)
    clean_text = re.sub(".*" + "Check email", '', clean_text)
    clean_text = re.sub(".*" + "Headlines email", '', clean_text)

    # msnbc pattern removal
    clean_text = re.sub("Tweet us " + ".*",'',clean_text)
    clean_text = re.sub("You can read more" + ".*",'', clean_text)

    #greenwich & ourmidland time pattern removal
    clean_text = re.sub("This is a carousel. Use Next and Previous buttons to navigate",'',clean_text)
    clean_text = re.sub("Show More",'',clean_text)
    clean_text = re.sub("Show Less",'',clean_text)

    #NJ.com
    clean_text = re.sub("Our journalism needs your support" + ".*",'',clean_text)
    clean_text = re.sub("For NJ Advance",'',clean_text)
    clean_text = re.sub("COPYRIGHT 2023 CREATORS.COM",'',clean_text)
    clean_text = re.sub("Thank you for relying on us to provide" + ".*",'',clean_text)
    clean_text = re.sub("RELATED STORIES " + ".*",'',clean_text)
    clean_text = re.sub("The N.J. High School Sports newsletter" + ".*",'',clean_text)

    #nbcsports
    clean_text = re.sub("Subscribe to and rate" + ".*",'',clean_text)
    clean_text = re.sub(" Click here to follow the " + ".*",'',clean_text)
    clean_text = re.sub(" Download and follow the" + ".*",'',clean_text)

    #newsweek
    clean_text = re.sub("(}[\s]*Getty[\s]*{)",'}{',clean_text)
    clean_text = re.sub("Newsweek reached out to" + ".*",'',clean_text)
    clean_text = re.sub("Newsweek has reached out to" + ".*",'',clean_text)

    #click2houston
    #pattern_c2 = "___" + ".*"
    #clean_text = re.sub(pattern_c2,'',clean_text)

    #clickorlando
    clean_text = re.sub("Get today’s headlines in minutes with",'',clean_text)
    clean_text = re.sub("Your Florida Daily",'',clean_text)
    clean_text = re.sub("Click here for more information about" + ".*",'',clean_text)
    clean_text = re.sub("FILE - ",'',clean_text)

    #cleveland.com
    clean_text = re.sub(" See video of the play here ",'',clean_text)
    clean_text = re.sub("Get police blotters by email every weekday for free with our new Police Blotter newsletter."  + ".*",'',clean_text)
    clean_text = re.sub("Ad not displaying properly?" + ".*",'',clean_text)
    clean_text = re.sub("Get a jumpstart on the weekend. Sign up for Cleveland.com ’s" + ".*",'',clean_text)
    clean_text = re.sub("Read more of her work" + ".*",'',clean_text)

    #nbcboston
    clean_text = re.sub("Get Boston local news, weather forecasts, lifestyle and entertainment stories to your inbox.","",clean_text)
    clean_text = re.sub("’s newsletters.","",clean_text)
    clean_text = re.sub("Read the full story on NBCNews.com here.","",clean_text)
    clean_text = re.sub("Get Boston local news, weather forecasts, lifestyle and entertainment stories to your inbox. ’s newsletters.",'',clean_text)

    #nbcchicago
    clean_text = re.sub("Get Chicago local news, weather forecasts, sports and entertainment stories to your inbox.","",clean_text)
    clean_text = re.sub("Read the full story on NBCNews.com here.","",clean_text)
    clean_text = re.sub("Download MyTeams Today!","",clean_text)
    clean_text = re.sub("""(}[\s]*Click here to)+[a-zA-Z=".\s\d&#-;,|<>:_'’]*({)""","",clean_text)
    clean_text = re.sub("Be sure to download the NBC Chicago app on your Apple or Android devices , or you can tune into the NBC 5 newscasts throughout the afternoon for the latest weather information.","",clean_text)
    clean_text = re.sub("For all the latest information, stay tuned to the NBC"+".*",'',clean_text)

    #nbcdfw
    clean_text = re.sub("Read the full story at NBCNews.com","",clean_text)
    clean_text = re.sub("Editor's note: All odds are provided by our partner, PointsBet ."+".*","",clean_text)
    clean_text = re.sub(" This story first appeared on TODAY.com . More from TODAY: ","",clean_text)

    #cnbc
    clean_text = re.sub("Subscribe\xa0 here \xa0to get this report sent directly to your inbox each morning before markets open. ","",clean_text)
    clean_text = re.sub("watch now","",clean_text)
    clean_text = re.sub("Getty Images Entertainment | Getty Images","",clean_text)

    #wgntv
    clean_text = re.sub("Suggest a Correction","",clean_text)
    clean_text = re.sub("This is a developing story, follow"+".*","",clean_text)

    #fox2news
    clean_text = re.sub("You can find out more at"+".*","",clean_text)
    clean_text = re.sub("This story will be updated throughout the day.","",clean_text)
    clean_text = re.sub(r"The Conversation","",clean_text)
    clean_text = re.sub(r'(-)+', r'\1',clean_text)

    #nbcmiami
    clean_text = re.sub("Get South Florida local news, weather forecasts and entertainment stories to your inbox.","",clean_text)
    clean_text = re.sub(" More information on how to apply can be found here .","",clean_text)
    clean_text = re.sub("This story first appeared on TODAY.com."+".*","",clean_text)

    clean_text = re.sub('\|*(Image source, )\|*','',clean_text) #removing bbc errors
    clean_text = re.sub('\|*(Image caption, )\|*','',clean_text) #removing bbc errors
    clean_text = re.sub('\|*(More on this story)\|*.+','',clean_text) #removing bbc errors
    clean_text = re.sub('\|*(Sign up for )\|*[a-z\sA-Z]+','',clean_text) #removing bbc errors
    clean_text = re.sub('\|*(Sign up to )\|*[a-z\sA-Z]+','',clean_text) #removing bbc errors

    clean_text = re.sub('\|*(This content is created and maintained by a third party, )\|*.+','',clean_text) #removing cosmopliton error
    clean_text = re.sub('\|*(Download it for )\|*[a-z\sA-Z]+','',clean_text) #removing cosmopliton error
    clean_text = re.sub('({Android})','{}',clean_text) #removing cosmopliton error
    #clean_text = re.sub('(Follow )+\S+( on ).+','',clean_text) #removing cosmopliton error
    #clean_text = re.sub('(>Instagram<)','><',clean_text) #removing Advertisement keyword

    clean_text = re.sub('\|*(A version of this story appeared in the )\|*[a-z\sA-Z0-9.]+','',clean_text) #removing hollywood error
    clean_text = re.sub('\|*(Click here to subscribe.)\|*','',clean_text) #removing hollywood error

    clean_text = re.sub('\|*(For weekly email updates on\nresidential real estate news, )\|*.+','',clean_text) #removing nytimes error


    clean_text = re.sub("""(}[\s]*(More News)+[Õa-zA-Z=".\s\d&#-;,:_'?|@’!~`$%^&*“”(){}<>\-_=+\[\]]+)""",'}',clean_text) #removing stamfordadvocate error of entire text after sentence starting with "More News" keyword
    clean_text = re.sub("""(}[\s]*(More Entertainment)+[Õa-zA-Z=".\s\d&-;,:_'?|@#’!~`$%^&*“”(){}<>\-_=+\[\]]+)""",'}',clean_text) #removing stamfordadvocate error of entire text after sentence starting with "More Entertainment" keyword
    clean_text = re.sub("""({p}}[\s]*(UP NEXT)+[Õa-zA-Z=".\s\d&-;,:_'?|@#’!~`$%^&*“”(){}<>\-_=+\[\]]+)""",'',clean_text) #removing stamfordadvocate error of entire text after sentence starting with "UP NEXT" keyword
    clean_text = re.sub("""(}[\s]*(___)+[Õa-zA-Z=".\s\d&-;,:_'?|@#’!~`$%^&*“”(){}<>\-_=+\[\]]+)""",'}',clean_text) #removing stamfordadvocate error of entire text after sentence starting with "___" keyword
    clean_text = re.sub('\|*(This is a carousel. Use Next and Previous buttons to navigate)\|*','',clean_text) #removing stamfordadvocate error

    #clean_text = re.sub("\|*(Top news)\|*[a-z</>\sA-Z'-.0-9:_‘’|“”$–?.-…{}]+",'',clean_text) #removing thegurdian error

    clean_text = re.sub('\|*(Required reading)\|*','',clean_text) #removing theatheletic error
    clean_text = re.sub("\|*(GO DEEPER{)\|*[/}a-zA-Z\s,'0-9:]+",'',clean_text) #removing theatheletic error

    clean_text = re.sub("\|*([A-Z])\|*[A-Z0-9\s',:.-]{20,}",'',clean_text) #removing foxnews error
    clean_text = re.sub("(NEW{)+[/a-zA-Z\s}!]+",'',clean_text) #removing foxnews error
    clean_text = re.sub('(}[\s]*Advertising[\s]*{)','}{',clean_text) #removing "Advertising" keyword

    clean_text = re.sub('(}[\s]*Advertising[\s]*{)','}{',clean_text) #removing "Advertising" keyword
    clean_text = re.sub("""([\s]*Also read[\s]*{/p})+[a-zA-Z{}=".\s\d&#-;,|<>:_'].+({/p})""",'',clean_text) #removing one para after "Also read" keyword
    clean_text = re.sub('(For more lifestyle news).+','',clean_text) #removing text after "For more lifestyle news" keyword
    clean_text = re.sub('(}[\s]*\(With inputs from agencies\)[\s]*{)','}{',clean_text) #removing "(With inputs from agencies)" keywords
    clean_text = re.sub('(({p}[\s]*Read)+[a-zA-Z{}=".\s\d&#-;,<>]+(on The Eastern Herald.))+[a-zA-Z{}=".\s\d&#-;,<>]+','',clean_text) #removing Last Lines in Eastern Herald keyword
    clean_text = re.sub("""(\{p\}\{strong\}[\s]*Also Read \|)+[a-zA-Z{}=".\s\d&#-;,<>:'?|@!~`$%^&*()_=+\[\]]+(\{/strong\}\{/p\})""",'',clean_text) #removing one para after "Also Read" keyword
    clean_text = re.sub("""({p}[\s]*SHARE THIS ARTICLE ON[\s]*{/p})+[a-zA-Z{}=".\s\d&#-;,*^@$!()+\[\]~`<>:_'\n?%]+""",'',clean_text) #removing text after "SHARE THIS ARTICLE ON" keyword
    clean_text = re.sub("""(\([\s]*Also read \|)+[a-zA-Z{}=".\s\d&#-;,<>:_']+(\))""",'',clean_text) #removing one para after "Also read |" keyword
    clean_text = re.sub("""(}[\s]*Also read:)+[a-zA-Z{}=".\s\d&#-;,<>:_']+({/a}{/p})""",'}',clean_text) #removing one para after "Also read:" keyword
    clean_text = re.sub("""(}[\s]*ALSO READ:)+[a-zA-Z{}=".\s\d&#-;,<>:_']+({/a}{/p})""",'}',clean_text) #removing one para after "ALSO READ: " keyword
    clean_text = re.sub("""(}[\s]*Also Read:)+[a-zA-Z{}=".\s\d&#-;,<>:_']+{/a}{/p}""",'}',clean_text) #removing one para after "ALSO READ: " keyword
    clean_text = re.sub("""(Also read \|)+[a-zA-Z{}=".\s\d&#-;,<>:_'?]+({/a})""",'',clean_text) #removing one para after "Also read |" keyword
    clean_text = re.sub("""([\s]*Source:)+[\sA-Za-z.]+""",'',clean_text) #removing "Source:" keyword
    clean_text = re.sub("""(}[\s]*top videos[\s]*{)""",'}{',clean_text) #removing "top videos" keyword
    clean_text = re.sub("""(ALSO READ\|)+[a-zA-Z{}=".\s\d&#-;,<>:_'?]+({/a})""",'',clean_text) #removing one para after "ALSO READ|" keyword
    clean_text = re.sub("""(}[\s]*Read all the)+[a-zA-Z{}=".\s\d&#-;,<>:()_]+(here[\s]*{/p})+[a-zA-Z{}=".\s\d&#-;,<>:()_]+""",'}',clean_text) #removing text after "Read all the ... here" keyword

    clean_text = re.sub("""(\{strong\}[\s]*ALSO READ \|)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+\{/strong\}""",'',clean_text) #removing one para after "ALSO READ |" keyword
    clean_text = re.sub("""(\{strong\}\{b\}[\s]*ALSO READ[\s]*\{/b\})+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+\{/strong\}""",'',clean_text) #removing one para after "ALSO READ |" keyword
    clean_text = re.sub('(}[\s]*advertisement[\s]*{)','}{',clean_text) #removing "advertisement" keyword
    clean_text = re.sub("""(}--- ENDS ---{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "--- ENDS ---" keyword
    clean_text = re.sub("""(}[\s]*Read here:)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+{/a}{/p}""",'}',clean_text) #removing "Read here:" keyword
    clean_text = re.sub("""(}[\s]*\(With inputs from ANI\)[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "(With inputs from ANI)" keyword
    clean_text = re.sub("""(}[\s]*\(With PTI inputs\)[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "(With PTI inputs)" keyword
    clean_text = re.sub("""(}[\s]*ABOUT THE AUTHOR[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "(ABOUT THE AUTHOR)" keyword
    clean_text = re.sub("""(\{strong\}[\s]*Also Read \|)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+\{/strong\}\{/a\}""",'',clean_text) #removing one para after "Also Read |" keyword
    clean_text = re.sub("""(}[\s]*\(With inputs from PTI, ANI\)[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "(With PTI inputs)" keyword

    # display(clean_text)
    clean_text = re.sub(r'{p}{strong}Watch This Story:&#160;{/strong}.*?{/strong} {/p}', '', clean_text, flags=re.DOTALL)

    clean_text = re.sub("""(\{p\}\{strong\}[\s]*WATCH \|[\s]*\{/strong\}\{/p\})""",'',clean_text) #removing "WATCH |" keyword
    clean_text = re.sub("""(\{p\}\{strong\}[\s]*ALSO WATCH \|[\s]*\{/strong\}\{/p\})""",'',clean_text) #removing "WATCH |" keyword
    clean_text = re.sub("""(}[\s]*ADVERTISEMENT[\s]*{)""",'}{',clean_text) #removing "ADVERTISEMENT" keyword
    clean_text = re.sub("""(}[\s]*Express News Service[\s]*{)""",'}{',clean_text) #removing "Express News Service" keyword
    clean_text = re.sub("""(}[\s]*Online Desk[\s]*{)""",'}{',clean_text) #removing "Online Desk" keyword
    clean_text = re.sub(""".+([\s]*By[\s]*{)""",'{',clean_text) #removing text before "By" keyword
    clean_text = re.sub("""(}[\s]*AFP[\s]*{)""",'}{',clean_text) #removing "AFP" keyword
    clean_text = re.sub("""(}[\s]*PTI[\s]*{)""",'}{',clean_text) #removing "PTI" keyword
    clean_text = re.sub("""(}[\s]*ANI[\s]*{)""",'}{',clean_text) #removing "ANI" keyword
    clean_text = re.sub("""(}[\s]*IANS[\s]*{)""",'}{',clean_text) #removing "IANS" keyword
    #clean_text = re.sub("""(}[\s]*View this post on Instagram[\s]*{)""",'}{',clean_text) #removing text "View this post on Instagram" keyword
    clean_text = re.sub("""(}[\s]*Latest Entertainment News[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "(With PTI inputs)" keyword
    #clean_text = re.sub("""([\s]*Follow us on Image Source INSTAGRAM[\s]*{)""",'{',clean_text) #removing text "Follow us on Image Source INSTAGRAM" keyword
    #clean_text = re.sub("""([\s]*Follow us on Image Source TWITTER[\s]*{)""",'{',clean_text) #removing text "Follow us on Image Source TWITTER" keyword
    clean_text = re.sub("""(}[\s]*Read More Trending News[\s]*{)""",'}{',clean_text) #removing text "Read More Trending News" keyword
    clean_text = re.sub("""(}[\s]*Here's how they reacted.[\s]*{)""",'}{',clean_text) #removing text "Here's how they reacted." keyword
    clean_text = re.sub("""(}[\s]*Check out the photos here-[\s]*{)""",'}{',clean_text) #removing text "Check out the photos here-" keyword
    clean_text = re.sub("""(}[\s]*Unsplash[\s]*{)""",'}{',clean_text) #removing "Unsplash" keyword
    clean_text = re.sub("""(}[\s]*Screenshot[\s]*{)""",'}{',clean_text) #removing "Screenshot" keyword
    clean_text = re.sub("""(}[\s]*screenshot[\s]*{)""",'}{',clean_text) #removing "screenshot" keyword
    clean_text = re.sub("""(}[\s]*Agencies[\s]*{)""",'}{',clean_text) #removing "Agencies" keyword
    #clean_text = re.sub("""(}[\s]*Twitter[\s]*{)""",'}{',clean_text) #removing "Twitter" keyword
    #clean_text = re.sub("""(}[\s]*TWITTER[\s]*{)""",'}{',clean_text) #removing "TWITTER" keyword
    #clean_text = re.sub("""(}[\s]*Reddit[\s]*{)""",'}{',clean_text) #removing "Reddit" keyword
    #clean_text = re.sub("""(}[\s]*Instagram[\s]*{)""",'}{',clean_text) #removing "Instagram" keyword
    #clean_text = re.sub("""(}[\s]*INSTAGRAM[\s]*{)""",'}{',clean_text) #removing "INSTAGRAM" keyword
    #clean_text = re.sub("""(}[\s]*Facebook[\s]*{)""",'}{',clean_text) #removing "Facebook" keyword
    #clean_text = re.sub("""(}[\s]*FACEBOOK[\s]*{)""",'}{',clean_text) #removing "FACEBOOK" keyword
    #clean_text = re.sub("""(}[\s]*Telegram[\s]*{)""",'}{',clean_text) #removing "Telegram" keyword
    #clean_text = re.sub("""(}[\s]*TELEGRAM[\s]*{)""",'}{',clean_text) #removing "TELEGRAM" keyword
    clean_text = re.sub("""(}[\s]*web screen grab[\s]*{)""",'}{',clean_text) #removing "web screen grab" keyword
    clean_text = re.sub("""(}[\s]*Reuters[\s]*{)""",'}{',clean_text) #removing "Reuters" keyword
    clean_text = re.sub("""(}[\s]*What do you think about it? Do let us know in the comments.[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "What do you think about it? Do let us know in the comments." keyword
    clean_text = re.sub("""(}[\s]*Click here .[\s]*{)""",'}{',clean_text) #removing "Click here ." keyword

    clean_text = re.sub("""(}[\s]*Poll[\s]*{)+[{}a-z/\s]+(}[\s]*0 votes[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "Poll 0 votes" keyword
    clean_text = re.sub("""([\s]*Leave your thoughts in the comments section below.[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'',clean_text) #removing text after "Leave your thoughts in the comments section below." keyword
    clean_text = re.sub("""(}[\s]*Check out the full video below[\s]*{)""",'}{',clean_text) #removing "Check out the full video below" keyword
    #clean_text = re.sub("""(\}[\s]*Read all the \{strong\} Latest News \{/strong\}, \{strong\} Trending News \{/strong\}, \{strong\} Cricket News \{/strong\}, \{strong\} Bollywood News \{/strong\}, \{strong\} India News \{/strong\} and \{strong\} Entertainment News \{/strong\} here. Follow us on Facebook , Twitter and Instagram .\{/p\})""",'}',clean_text) #removing "Read all the Latest News , Trending News , Cricket News , Bollywood News , India News and Entertainment News here. Follow us on Facebook , Twitter and Instagram ." keyword
    clean_text = re.sub("""(}[\s]*Related[\s]*{)""",'}{',clean_text) #removing "Related" keyword
    clean_text = re.sub("""({b}IPL 2023{/b} {b} . {/b} {b}Dream11 Prediction{/b} {b} . {/b} {b}Fantasy Cricket Tips{/b} {b} . {/b} {b}Cricket Match Prediction Today{/b} {b} . {/b} {b}Cricket News{/b} {b} . {/b} {b}Cricket Live Score{/b})""",'',clean_text) #removing "IPL 2023 . Dream11 Prediction . Fantasy Cricket Tips . Cricket Match Prediction Today . Cricket News . Cricket Live Score" keyword
    clean_text = re.sub("""({b}IPL 2023{/b} {b} .{/b} {b}India National Cricket Team{/b} {b}. {/b} {b}Chennai Super Kings {/b} {b} . {/b} {b}Delhi Capitals {/b} {b} . {/b} {b}Gujarat Titans {/b} {b} . {/b} {b}Kolkata Knight Riders {/b} {b} . {/b} {b}Lucknow Supergiants {/b} {b} . {/b} {b}Mumbai Indians {/b} {b} . {/b} {b}Punjab Kings {/b} {b} . {/b} {b}Rajasthan Royals {/b} {b} . {/b} {b}Royal Challengers Bangalore {/b} {b} . {/b} {b}SunRisers Hyderabad {/b})""",'',clean_text) #removing "IPL 2023 . India National Cricket Team . Chennai Super Kings . Delhi Capitals . Gujarat Titans . Kolkata Knight Riders . Lucknow Supergiants . Mumbai Indians . Punjab Kings . Rajasthan Royals . Royal Challengers Bangalore . SunRisers Hyderabad" keyword
    clean_text = re.sub("""({b}Virat Kohli{/b} {b} . {/b} {b}Rohit Sharma{/b} {b} . {/b} {b}Rishabh Pant{/b} {b} . {/b} {b}KL Rahul{/b} {b} . {/b} {b}Suryakumar Yadav{/b} {b} . {/b} {b}Sanju Samson{/b} {b} . {/b} {b}Shreyas Iyer{/b} {b} . {/b} {b}Yuzvendra Chahal{/b} {b} . {/b} {b}Jasprit Bumrah{/b})""",'',clean_text) #removing "Virat Kohli . Rohit Sharma . Rishabh Pant . KL Rahul . Suryakumar Yadav . Sanju Samson . Shreyas Iyer . Yuzvendra Chahal . Jasprit Bumrah" keyword
    clean_text = re.sub("""(}[\s]*Follow InsideSport on GOOGLE NEWS[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "Follow InsideSport on GOOGLE NEWS" keyword
    clean_text = re.sub("""(}[\s]*Here’s the video[\s]*{)""",'}{',clean_text) #removing "Here’s the video" keyword
    clean_text = re.sub("""(}[\s]*Here is the video[\s]*{)""",'}{',clean_text) #removing "Here is the video" keyword
    clean_text = re.sub("""(}[\s]*Stay tuned to BollywoodLife for the latest scoops and updates from Bollywood , Hollywood , South , TV and Web-Series .[\s]*{)""",'}{',clean_text) #removing "Stay tuned to BollywoodLife for the latest scoops and updates from Bollywood , Hollywood , South , TV and Web-Series ." keyword
    #clean_text = re.sub("""(}[\s]*Click to join us on Facebook , Twitter , Youtube and Instagram .[\s]*{)""",'}{',clean_text) #removing "Click to join us on Facebook , Twitter , Youtube and Instagram ." keyword
    #clean_text = re.sub("""(}[\s]*Also follow us on Facebook Messenger for latest updates.[\s]*{)""",'}{',clean_text) #removing "Also follow us on Facebook Messenger for latest updates." keyword
    clean_text = re.sub("""(}[\s]*Click Here To Read/Download Order[\s]*{)""",'}{',clean_text) #removing "Click Here To Read/Download Order" keyword
    clean_text = re.sub("""(}[\s]*Click Here To Read/Download Judgement[\s]*{)""",'}{',clean_text) #removing "Click Here To Read/Download Judgement" keyword

    clean_text = re.sub("""(}[\s]*View this post on Instagram[\s]*{)""",'}{',clean_text) #removing text "View this post on Instagram" keyword
    clean_text = re.sub("""(}[\s]*SHARE[\s]*{)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing text after "SHARE" keyword
    clean_text = re.sub("""(}[\s]*Also read)+[a-zA-Z{}=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]‘’]+({)""",'}{',clean_text) #removing text "Also read" keyword
    clean_text = re.sub("""(}[\s]*READ NOW[\s]*{)""",'}{',clean_text) #removing before "READ NOW" keyword
    clean_text = re.sub("""(}[\s]*Also read)""",'}',clean_text) #removing before "READ NOW" keyword

    clean_text = re.sub("""(}[\s]*Listen[\s]*{\/p})+[a-zA-Z=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+({\/p}[\s]*Comment[\s]*{\/p})""",'}',clean_text) #removing text between "Listen" and "Comment" keyword
    clean_text = re.sub("""([\s]*Comment[\s]*{)""",'{',clean_text) #removing "Comment" keyword
    clean_text = re.sub("""(}[\s]*Gift Article[\s]*{)""",'}{',clean_text) #removing "Gift Article" keyword
    clean_text = re.sub("""(}[\s]*Share[\s]*{)""",'}{',clean_text) #removing "Share" keyword
    clean_text = re.sub("""(}[\s]*Listen[\s]*{)""",'}{',clean_text) #removing "Listen" keyword
    clean_text = re.sub("""(}[\s]*ArrowRight[\s]*{)""",'}{',clean_text) #removing "ArrowRight" keyword
    clean_text = re.sub("""(}[\s]*Loading...[\s]*{)""",'}{',clean_text) #removing "Loading..." keyword
    clean_text = re.sub("""(}[\s]*Never miss a goal or a touchdown. .[\s]*{)""",'}{',clean_text) #removing "Never miss a goal or a touchdown. ." keyword
    clean_text = re.sub("""(}[\s]*Wp Get the full experience. Choose your plan[\s]*{)""",'}{',clean_text) #removing "Wp Get the full experience. Choose your plan" keyword

    clean_text = re.sub("""(}[\s]*SEE MORE:[\s]*)+[a-zA-Z=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing para starting with "SEE MORE:" keyword
    clean_text = re.sub("""(}[\s]*See More:[\s]*)+[a-zA-Z=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing para starting with "See More:" keyword
    clean_text = re.sub("""([\s]*Trending stories at Scrippsnews.com[\s]*{)""",'{',clean_text) #removing "Trending stories at Scrippsnews.com" keyword
    clean_text = re.sub("""(}[\s]*LOOK BACK:[\s]*)+[a-zA-Z=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing para starting with "LOOK BACK:" keyword
    clean_text = re.sub("""([\s]*Subscribe to our weekly newsletter, In The Know, to get entertainment news sent straight to your inbox.[\s]*{)""",'{',clean_text) #removing "Subscribe to our weekly newsletter, In The Know, to get entertainment news sent straight to your inbox." keyword
    clean_text = re.sub("""(}[\s]*©[\s]*)+[a-zA-Z=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing para starting with "©" keyword
    clean_text = re.sub("""(}[\s]*Copyright ©[\s]*)+[a-zA-Z=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing para starting with "Copyright ©" keyword

    clean_text = re.sub("""(}[\s]*Click to email a link to a friend \(Opens in new window\)[\s]*{)""",'}{',clean_text) #removing "Click to email a link to a friend (Opens in new window)" keyword
    #clean_text = re.sub("""(}[\s]*Click to share on Twitter \(Opens in new window\)[\s]*{)""",'}{',clean_text) #removing "Click to share on Twitter (Opens in new window)" keyword
    #clean_text = re.sub("""(}[\s]*Click to share on Facebook \(Opens in new window\)[\s]*{)""",'}{',clean_text) #removing "Click to share on Facebook (Opens in new window)" keyword
    clean_text = re.sub("""(}[\s]*For more Page Six[\s]*)+[a-zA-Z=".\s\d&#-;,<>:_'?|@#!~`$%^&*()\-_=+\[\]]+""",'}',clean_text) #removing para starting with "For more Page Six" keyword

    clean_text = re.sub("""(}[\s]*Get the inside scoop on today’s biggest stories in business, from Wall Street to Silicon Valley — delivered daily.[\s]*{)""",'}{',clean_text) #removing "Get the inside scoop on today’s biggest stories in business, from Wall Street to Silicon Valley — delivered daily." keyword
    clean_text = re.sub("""(}[\s]*Loading Something is loading.[\s]*{)""",'}{',clean_text) #removing "Loading Something is loading." keyword
    clean_text = re.sub("""(}[\s]*Thanks for signing up![\s]*{)""",'}{',clean_text) #removing "Thanks for signing up!" keyword
    clean_text = re.sub("""(}[\s]*Access your favorite topics in a personalized feed while you're on the go.[\s]*{)""",'}{',clean_text) #removing "Access your favorite topics in a personalized feed while you're on the go." keyword
    clean_text = re.sub("""(}[\s]*Email address[\s]*{)""",'}{',clean_text) #removing "Email address" keyword
    clean_text = re.sub("""(}[\s]*By clicking ‘Sign up’, you agree to receive marketing emails from Insider as well as other partner offers and accept our Terms of Service and Privacy Policy[\s]*{)""",'}{',clean_text) #removing "By clicking ‘Sign up’, you agree to receive marketing emails from Insider as well as other partner offers and accept our Terms of Service and Privacy Policy" keyword

    clean_text = re.sub("""(}[\s]*Enlarge this image[\s]*{)""",'}{',clean_text) #removing "Enlarge this image" keyword
    clean_text = re.sub("""({b}*toggle caption[\s]*{/b}{/b}[\s]*{/p}[\sa-zA-Z\d/]*{/p})""",'',clean_text) #removing "toggle caption" keyword and one para after that keyword
    clean_text = re.sub("""(}[\s]*(Email us at)+[Õa-zA-Z=".\s\d&#-;,<>:_'?|@“#!~`’$%^&*()\-_=+\[\]]+{)""",'}{',clean_text) #removing sentence starting with "Email us at" keyword

    clean_text = re.sub("""(}[\s]*[\[\]\d/]+[Õa-zA-Z=".\s\d&#-;,<>:_'?|@“#!~`$%^&’*()\-_=+\[\]]+{)""",'}{',clean_text) #removing sentence starting with "[1/8]" or [1:4] etc. keyword
    clean_text = re.sub("""(}[\s]*Our Standards: The Thomson Reuters Trust Principles.[\s]*{)""",'}{',clean_text) #removing "Our Standards: The Thomson Reuters Trust Principles." keywords

    clean_text = re.sub("""(}[\s]*(Reporting by)+[Õa-zA-Z=".\s\d&#-;,:_'?|“@#!~`$%^&*’(){}<>\-_=+\[\]]+)""",'}',clean_text) #removing entire text after sentence starting with "Reporting by" keyword
    clean_text = re.sub("""(}[\s]*(Editing by)+[Õa-zA-Z=".\s\d&#-;,:_'?|@“#!~`$%^&*’(){}<>\-_=+\[\]]+)""",'}',clean_text) #removing entire text after sentence starting with "Editing by" keyword
    clean_text = re.sub("""(}[\s]*-Field Level Media[\s]*{)""",'}{',clean_text) #removing "-Field Level Media" keyword
    clean_text = re.sub("""(}[\s]*- Field Level Media[\s]*{)""",'}{',clean_text) #removing "- Field Level Media" keyword
    clean_text = re.sub("""(}[\s]*The opinions expressed here are those of the author, a columnist for Reuters.[\s]*{)""",'}{',clean_text) #removing "The opinions expressed here are those of the author, a columnist for Reuters." keyword

    clean_text = re.sub("""(}[\s]*LOADING[\s]*{)""",'}{',clean_text) #removing "LOADING" keyword
    clean_text = re.sub("""(}[\s]*Loading[\s]*{)""",'}{',clean_text) #removing "Loading" keyword
    clean_text = re.sub("""(}[\s]*loading[\s]*{)""",'}{',clean_text) #removing "loading" keyword
    clean_text = re.sub("""(}[\s]*ERROR LOADING[\s]*{)""",'}{',clean_text) #removing "ERROR LOADING" keyword
    clean_text = re.sub("""(}[\s]*Error Loading[\s]*{)""",'}{',clean_text) #removing "Error Loading" keyword
    clean_text = re.sub("""(}[\s]*error loading[\s]*{)""",'}{',clean_text) #removing "error loading" keyword
    clean_text = re.sub("""(}[\s]*‘’[\s]*{)""",'}{',clean_text) #removing "error loading" keyword

    clean_text = re.sub("""(}[\s]*Show Caption[\s]*{)""",'}{',clean_text) #removing "Show Caption" keyword
    clean_text = re.sub("""(}[\s]*Hide Caption[\s]*{)""",'}{',clean_text) #removing "Hide Caption" keyword
    clean_text = re.sub("""(}[\s]*Accuweather[\s]*{)""",'}{',clean_text) #removing "Accuweather" keyword
    clean_text = re.sub("""(}[\s]*AP[\s]*{)""",'}{',clean_text) #removing "AP" keyword
    clean_text = re.sub("""(}[\s]*(Contributing:)+[Õa-zA-Z=".\s\d&#-;,<>:_'?|“@#’!~`$%^&*()\-_=+\[\]]+{)""",'}{',clean_text) #removing sentence starting with "Contributing:" keyword
    clean_text = re.sub("""(}[\s]*(Follow USA TODAY)+[Õa-zA-Z=".\s\d&#-;,<>:_'?|’@“#!~`$%^&*()\-_=+\[\]]+{)""",'}{',clean_text) #removing sentence starting with "Follow USA TODAY" keyword
    clean_text = re.sub("""(({strong}[\s]*Watch )+[Õa-zA-Z=".\s\d&#-;,<>:_'?|“@#!~’`$%^&*()\-_=+\[\]]+{/strong})""",'',clean_text) #removing sentence starting with "<strong>Watch" keyword

    clean_text = re.sub("""(}[\s]*(Check out:)+[Õa-zA-Z=".\s\d&#-;,:_'?|@“#!~`$%^&*()’{}<>\-_=+\[\]]+)""",'}',clean_text) #removing entire text after sentence starting with "Check out" keyword
    clean_text = re.sub("""(}[\s]*(CHECK OUT:)+[Õa-zA-Z=".\s\d&#-;,:_'?|@“#!~`$%^&*()’{}<>\-_=+\[\]]+)""",'}',clean_text) #removing entire text after sentence starting with "CHECK OUT" keyword
    clean_text = re.sub("""(}[\s]*(check out:)+[Õa-zA-Z=".\s\d&#-;,:_'?|@“#!~`$%^&*()’{}<>\-_=+\[\]]+)""",'}',clean_text) #removing entire text after sentence starting with "check out" keyword
    clean_text = re.sub("""(}[\s]*(Check Out:)+[Õa-zA-Z=".\s\d&#-;,:_'?|@“#!~`$%^&*’(){}<>\-_=+\[\]]+)""",'}',clean_text) #removing entire text after sentence starting with "Check Out" keyword
    clean_text = re.sub("""(}[\s]*(DON'T MISS:)+[Õa-zA-Z=".\s\d&#-;,:_'?|@“#!~`$%^’&*(){}<>\-_=+\[\]]+)""",'}',clean_text) #removing entire text after sentence starting with "DON'T MISS:" keyword
    clean_text = re.sub("""(}[\s]*(don't miss:)+[Õa-zA-Z=".\s\d&#-;,:_'?|@“#!~`$%’^&*(){}<>\-_=+\[\]]+)""",'}',clean_text) #removing entire text after sentence starting with "don't miss:" keyword
    clean_text = re.sub("""(}[\s]*(Don't Miss:)+[Õa-zA-Z=".\s\d&#-;,:_'?|@“#!~`$’%^&*(){}<>\-_=+\[\]]+)""",'}',clean_text) #removing entire text after sentence starting with "Don't Miss:" keyword
    clean_text = re.sub("""(}[\s]*(Don't miss:)+[Õa-zA-Z=".\s\d&#-;,:_'?|@“#!~`’$%^&*(){}<>\-_=+\[\]]+)""",'}',clean_text) #removing entire text after sentence starting with "Don't miss:" keyword
    clean_text = re.sub("""(}[\s]*In this article[\s]*{)""",'}{',clean_text) #removing "In this article" keyword
    clean_text = re.sub("""(}[\s]*(Get CNBC's free)+[Õa-zA-Z=".\s\d&“#-;,<>:_'?|@’#!~`$%^&*()\-_=+\[\]]+{)""",'}{',clean_text) #removing sentence starting with "Get CNBC's free" keyword
    clean_text = re.sub("""(}[\s]*(Like this story)+[Õa-zA-Z=".\s\d&“#-;,<>:_'?|’@#!~`$%^&*()\-_=+\[\]]+{)""",'}{',clean_text) #removing sentence starting with "Like this story" keyword
    clean_text = re.sub("""(}[\s]*(This report)+[Õa-zA-Z=".\s\d&“#-;,<>:_'?|@#!’~`$%^&*()\-_=+\[\]]+{)""",'}{',clean_text) #removing sentence starting with "This report" keyword
    clean_text = re.sub("""(}[\s]*[A-Z]{1,5}[\s]*{)""",'}{',clean_text) #removing keywords with with length between 1 to 5

    #clean_text = re.sub("""(}[\s]*(Follow us on Twitter)+[Õa-zA-Z=".\s\d&#-;,:_'?|@“#’!~`$%^&*(){}<>\-_=+\[\]]+)""",'}',clean_text) #removing entire text after sentence starting with "Follow us on Twitter" keyword
    clean_text = re.sub("""(}[\s]*(Presented by)+[Õa-zA-Z=".\s\d&#-;,<>:_'?|@“#!~`$%’^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "Presented by" keyword
    clean_text = re.sub("""(}[\s]*(Presented By)+[Õa-zA-Z=".\s\d&#-;,<>:_'?|@“#!~`$’%^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "Presented By" keyword
    clean_text = re.sub("""(}[\s]*(PRESENTED BY)+[Õa-zA-Z=".\s\d&#-;,<>:_'?|@“#!~`’$%^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "PRESENTED BY" keyword
    clean_text = re.sub("""(}[\s]*(FOLLOW US)+[Õa-zA-Z=".\s\d&#-;,<>:_'?|@“#!~`$%’^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "FOLLOW US++++" keyword
    clean_text = re.sub("""(}[\s]*(Follow Us)+[Õa-zA-Z=".\s\d&#-;,<>:_'?|@“#!~`$’%^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "Follow Us" keyword
    clean_text = re.sub("""(}[\s]*(Follow us)+[Õa-zA-Z=".\s\d&#-;,<>:_'?|@“#!~`’$%^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "Follow us" keyword

    # This code given below
    # clean_text = re.sub("""(}[\s]*(For more information)+[Õa-zA-Z=".\s\d&“#-;,<>:_'?|@’#!~`$%^&*()\-_=+\[\]]+{)""",'}{',clean_text) #removing sentence starting with "For more information" keyword
    clean_text = re.sub("""(}[\s]*(Copyright)+[Õa-zA-Z=".\s\d&#-;,<>:_'?|@’#“!~`$%^&*()\-_=+\[\]]+{)""",'}{',clean_text) #removing sentence starting with "Copyright" keyword

    clean_text = re.sub("""(}[\s]*With News Wire Services[\s]*{)""",'}{',clean_text) #removing "With News Wire Services" keyword
    clean_text = re.sub("""(}[\s]*The Pinstripe Express[\s]*{)""",'}{',clean_text) #removing "The Pinstripe Express" keyword
    clean_text = re.sub("""(}[\s]*Weekly[\s]*{)""",'}{',clean_text) #removing "Weekly" keyword
    clean_text = re.sub("""(}[\s]*(The Daily News )+[Õa-zA-Z=".\s\d&#-;,<>:_'?|@“#!~`$’%^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "The Daily News " keyword
    clean_text = re.sub("""(}[\s]*(By submitting your email)+[Õa-zA-Z=".\s\d&“#-;,<>:_'?|@#!~`$’%^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "By submitting your email" keyword
    #clean_text = re.sub("""(}[\s]*The Daily News Flash[\s]*{)""",'}{',clean_text) #removing "The Daily News Flash" keyword
    clean_text = re.sub("""(}[\s]*Weekdays[\s]*{)""",'}{',clean_text) #removing "Weekdays" keyword
    clean_text = re.sub("""(}[\s]*(Catch up on )+[Õa-zA-Z=".\s\d&“#-;,<>:_'?|@#!~`$’%^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "Catch up on " keyword
    clean_text = re.sub("""(}[\s]*Breaking News[\s]*{)""",'}{',clean_text) #removing "Breaking News" keyword
    clean_text = re.sub("""(}[\s]*As it happens[\s]*{)""",'}{',clean_text) #removing "As it happens" keyword
    clean_text = re.sub("""(}[\s]*(Get updates on )+[Õa-zA-Z=".\s\d&#-;,<>:_'?|“@#!~`$’%^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "Get updates on " keyword
    clean_text = re.sub("""(}[\s]*(\[)+[Õa-zA-Z=".\s\d&#-;,<>:_'?|“@#!~`$’%^&*()\-_=+\[\]]*(\])+[\s]*{)""",'}{',clean_text) #removing sentence starting with "[" and ending with "]" keywords

    clean_text = re.sub("""(}[\s]*(Never miss a story)+[Õa-zA-Z=".\s\d&#-;,<>'?|“@#!~`$’%—^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "Never miss a story" keyword
    clean_text = re.sub("""({p}[\s]*[A-Z\s/.:]+{\/p})""",'',clean_text) #removing paragraph having  all caps and / and space and . AND :
    clean_text = re.sub("""(}[\s]*(Write to)+[Õa-zA-Z=".\s\d&#-;,<>'?|“@#!~`$’%—^&*()\-_=+\[\]]*)""",'}',clean_text) #removing sentence starting with "Write to" keyword
    clean_text = re.sub("""(}[\s]*(By )+[A-Za-z]*[\s]*[A-Za-z]*[\s]*[A-Za-z]{)""",'}{',clean_text) #removing sentence starting with "Write to" keyword

    clean_text = re.sub("""(}[\s]*(Follow )+[Õa-zA-Z=".\s\d&#-;,<>'?|@“#!~`$’%—^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "Follow " keyword
    clean_text = re.sub("""(}[\s]*(FOLLOW )+[Õa-zA-Z=".\s\d&#-;,<>'?|@“#!~`$’%—^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "FOLLOW " keyword
    clean_text = re.sub("""(}[\s]*[\d]*[\s]*{)""",'}{',clean_text) #removing para with numbers only keyword
    clean_text = re.sub("""(}[\s]*(View Profile)+[Õa-zA-Z=".\s\d&“#-;,<>'?|@#!~`$’%—^&*()\-_=+\[\]]*)""",'}',clean_text) #removing sentence starting with "View Profile" keyword
    clean_text = re.sub("""((Watch :)+[Õa-zA-Z=".\s\d&#-;,<>'?|@“#!~`$’%—^&*()\-_=+\[\]]*{)""",'{',clean_text) #removing sentence starting with "Watch :" keyword
    clean_text = re.sub("""((Watch:)+[Õa-zA-Z=".\s\d&#-;,<>'?|@“#!~`$’%—^&*()\-_=+\[\]]*{)""",'{',clean_text) #removing sentence starting with "Watch:" keyword
    clean_text = re.sub("""((WATCH :)+[Õa-zA-Z=".\s\d&#-;,<>'?|@“#!~`$’%—^&*()\-_=+\[\]]*{)""",'{',clean_text) #removing sentence starting with "WATCH :" keyword
    clean_text = re.sub("""((WATCH:)+[Õa-zA-Z=".\s\d&#-;,<>'?|@“#!~`$’%—^&*()\-_=+\[\]]*{)""",'{',clean_text) #removing sentence starting with "WATCH:" keyword
    clean_text = re.sub("""(}[\s]*(Pick up )+[Õa-zA-Z=".\s\d&“#-;,<>'?|@#!~`$’%—^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "Pick up " keyword
    clean_text = re.sub("""(}[\s]*(PICK UP )+[Õa-zA-Z=".\s\d&“#-;,<>'?|@#!~`$’%—^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "PICK UP " keyword

    clean_text = re.sub("""(}[\s]*(Photo)+[\s]*(:)+[Õa-zA-Z=".\s\d&“#-;,<>'?|@#!~`$’%—^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "Photo :" or "Photo:" keyword
    clean_text = re.sub("""(}[\s]*(PHOTO)+[\s]*(:)+[Õa-zA-Z=".\s\d&“#-;,<>'?|@#!~`$’%—^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "PHOTO :" or "PHOTO:" keyword
    clean_text = re.sub("""(}[\s]*[A-Za-z]*[\s]*{)""",'}{',clean_text) #removin para with alphabets only keyword
    clean_text = re.sub("""(}[\s]*[Õa-zA-Z=".\s\d&#-;,'?|<>@“#!~`$’%—^&*()\-_=+\[\]]{2}[\s]*{)""",'}{',clean_text) #removin para with 2 length
    clean_text = re.sub("""(}[\s]*(Photograph by )+[Õa-zA-Z=".\s\d&“#-;,<>'?|@#!~`$’%—^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "Photograph by " keyword
    clean_text = re.sub("""(}[\s]*(PHOTOGRAPH BY )+[Õa-zA-Z=".\s\d&“#-;,<>'?|@#!~`$’%—^&*()\-_=+\[\]]*{)""",'}{',clean_text) #removing sentence starting with "PHOTOGRAPH BY " keyword
    clean_text = re.sub("""([\s]*(CLICK HERE)+[\s]*)""",'',clean_text) #removing text "CLICK HERE"
    clean_text = re.sub("""([\s]*(Click Here)+[\s]*)""",'',clean_text) #removing text "Click Here"
    clean_text = re.sub("""([\s]*(Click here)+[\s]*)""",'',clean_text) #removing text "Click here"
    clean_text = re.sub("""([\s]*(click here)+[\s]*)""",'',clean_text) #removing text "click here"

    clean_text = re.sub("""({i}[Õa-zA-Z=".\s\d&#-;,<>:_'?|@#!~`$’“%—^&*()\-’_=+\[\]]+{/i})""",'',clean_text) #removing i-tag sentence (specifically for FOX Business)
    clean_text = re.sub("""({i}[Õa-zA-Z=".\s\d&#-;,<>:_'?|@#!~`$’“%—^&*()\-’_=+\[\]]+{i})""",'',clean_text) #removing i-tag sentence (specifically for Forbes)



    # For vulture.com
    clean_text = re.sub(r'\s*Related{/h2}\s*', "", clean_text)
    clean_text = re.sub(r'\\n+', '\\n', clean_text)

    # For usmagazine
    clean_text = re.sub(r"Subscribe to newsletters.*?{/p}\n\s*\n\s*{/p}", "", clean_text, flags=re.DOTALL) # Removing the texts starting with "Subscribe to newsletters" and ending with "{/p}\n\s*\n\s*{/p}"
    clean_text = re.sub(r'\s*{p}You have successfully subscribed.{/p}\s*', "", clean_text) # Removing the words "You have successfully subscribed"
    clean_text = re.sub("Related:.*?\.\.\.", "", clean_text) # Removing the texts starting with "Related" and ending with "\t\t{/p}\n\t\n{p}"
    clean_text = re.sub("Related:.*?\t\t{/p}\n\t\n{p}", "{p}", clean_text)
    clean_text = re.sub(r'In this article{/h3}.*?{IMG_\d+}}{/h3}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'In this article{/h3}.*?{img src={IMG_\d+}}.*?{/h3}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}See it:.*?{/strong}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}Not what .*?!{/strong}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}See it: Get the.*?{/strong}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'Related: {/p}.*?\t\t{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'In this article.*?{/p}', '', clean_text, flags=re.DOTALL)

    # For einnews
    clean_text = re.sub("{p}Page Content{/p}", "", clean_text)
    clean_text = re.sub(r'{strong}Contacts:{/strong}.*?{img src={IMG_\d+}}{br}{img src={IMG_\d+}}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}Company Contacts:{/strong}.*?{img src={IMG_\d+}}{br}{img src={IMG_\d+}}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}Contact:{/strong}.*?{img src={IMG_\d+}}{br}{img src={IMG_\d+}}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'\\r', '', clean_text)
    clean_text = re.sub(r'{p}For more information, contact:{/p}.*?{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'&#226;&#128;&#162;', '•', clean_text)

    # For essentiallysports
    clean_text = re.sub("""(}[\s]*(Article continues below this)+[Õa-zA-Z=".\s\d&“#-;,<>:_'?|@’#!~`$%^&*()\-_=+\[\]]+{)""",'}{',clean_text)
    clean_text = re.sub("""(}[\s]*(America&#8217;s Favorite Video Toda)+[Õa-zA-Z=".\s\d&“#-;,<>:_'?|@’#!~`$%^&*()\-_=+\[\]]+{)""",'}{',clean_text)
    clean_text = re.sub("""(}[\s]*(Providing feedback will help us make your experience)+[Õa-zA-Z=".\s\d&“#-;,<>:_'?|@’#!~`$%^&*()\-_=+\[\]]+{)""",'}{',clean_text)
    clean_text = re.sub("""(}[\s]*(Enjoyed Your Read?)+[Õa-zA-Z=".\s\d&“#-;,<>:_'?|@’#!~`$%^&*()\-_=+\[\]]+{)""",'}{',clean_text)
    clean_text = re.sub(r'{p}Least Likely{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Most Likely{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub("""(}[\s]*(The Fan's Perspectiv)+[Õa-zA-Z=".\s\d&“#-;,<>:_'?|@’#!~`$%^&*()\-_=+\[\]]+{)""",'}{',clean_text)


    clean_text = re.sub("""(}[\s]*(For more information)+[Õa-zA-Z=".\s\d&“#-;,<>:_'?|@’#!~`$%^&*()\-_=+\[\]]+{)""",'}{',clean_text) #removing sentence starting with "For more information" keyword

    # fox26houston
    clean_text = re.sub(r'{strong}PREVIOUS: {/strong}.*?{/strong}', '',  clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}\(KUTV-TV via FOX\) {/p}', '', clean_text)
    clean_text = re.sub(r'{p}{i}{strong}Have a finance-related question.*?{/p}', "", clean_text, flags=re.DOTALL)
    # clean_text = re.sub(r'article{/p}{/p}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}RELATED: {/strong}{strong}.*?{/strong}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}EARLIER: {/strong}{strong}.*?{/strong}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}{strong}SUGGESTED: {/strong}{strong}.*?{/strong}{/p}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'SUGGESTED:  {strong}.*?{/strong}{/p}', "",clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}FOX 26 Houston is now.*?{/strong}', "", clean_text, flags=re.DOTALL)

    # For globalnews
    clean_text = re.sub(r'{p}Send this page to someone via email{/p}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}.*?Get the latest National news.*?{/strong}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'Story continues below advertisement{/p}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'View image in full screen{/p}', "", clean_text, flags=re.DOTALL)


    # For fox32chicago.com
    clean_text = re.sub(r'{strong}READ MORE:{/strong}{strong}.*?{/strong}', '', clean_text, flags=re.DOTALL)

    # For cbs4local
    clean_text = re.sub(r'{strong}RECOMMENDED: {/strong}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'to receive the top interesting stories from in and around our community once daily in your inbox.', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}{strong}READ MORE: {/strong}{/p}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}RECOMMENDED:{/strong}', "", clean_text, flags=re.DOTALL)

    # For fox7austin
    clean_text = re.sub(r'{p}{strong}MORE: {/strong}{strong}.*?{/strong}{/p}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}{strong}READ:{/strong}{strong}.*?{/strong}{/p}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}{strong}RELATED:{/strong}{strong}.*?{/strong}{/p}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}NASA&#8217;{/strong}', "", clean_text, flags=re.DOTALL)

    # For kearneyhub
    clean_text = re.sub(r'\d+{/p} Comments.*?{/p}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub("""(}[\s]*(Be the first to know)+[Õa-zA-Z=".\s\d&#-;,<>'?|@“#!~`$’%—^&*()\-_=+\[\]]*{)""", '}{', clean_text)
    clean_text = re.sub("""(}*[Õa-zA-Z=".\s\d&#-;,<>'?|@“#!~`$’%—^&*()\-_=+\[\]]+(Get local news delivered to your inbox)+[Õa-zA-Z=".\s\d&#-;,<>'?|@“#!~`$’%—^&*()\-_=+\[\]]*{)""", '}{', clean_text)
    clean_text = re.sub("""(}*[Õa-zA-Z=".\s\d&#-;,<>'?|@“#!~`$’%—^&*()\-_=+\[\]]+(I understand and agree that registration on or use of this site constitutes agreement to its user agreement and  privacy policy .)+[Õa-zA-Z=".\s\d&#-;,<>'?|@“#!~`$’%—^&*()\-_=+\[\]]*{)""", '}{', clean_text)
    clean_text = re.sub(r'Subscribe to our Daily Headlines newsletter.', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'} Obituaries Newsletter{', "}{", clean_text, flags=re.DOTALL)
    clean_text = re.sub(re.escape("* I understand and agree that registration on or use of this site constitutes agreement to its user agreement and  privacy policy ."), "", clean_text)
    clean_text = re.sub(re.escape("{/h2}\n                 .{/p}"), "", clean_text)
    clean_text = re.sub("""(}[\s]*(Get in the game with our)+[Õa-zA-Z=".\s\d&#-;,<>'?|@“#!~`$’%—^&*()\-_=+\[\]]*{)""", "}{", clean_text)
    clean_text = re.sub(r'Sent weekly directly to your inbox!', "", clean_text, flags=re.DOTALL)

    #For peoplenewspapers
    clean_text = re.sub(r'Share this article...', "", clean_text, flags=re.DOTALL)

    #For wftv.com
    clean_text = re.sub(r'{b}Read:.*?{/b}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}to download our free news, weather and smart TV apps. Andto stream Channel 9 Eyewitness News live.{', "}{", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'&#169;2024 Cox Media Group', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'&#169; 2024 Cox Media Group', "", clean_text, flags=re.DOTALL)

    # For ksat.com
    clean_text = re.sub(r'More UIL and Big Game Coverage on KSAT:', "", clean_text, flags=re.DOTALL)

    #For nme.com
    clean_text = re.sub(r'{p}{strong}{/strong}{br}\n{strong}{/strong}{br}\n{strong}{/strong}{br}\n{strong}{/strong}{br}\n{strong}{/strong}{br}\n{strong}{/strong}{br}\n{strong}{/strong}{br}\n{strong}{/strong}{br}\n{strong}{/strong}{br}\n{strong}{/strong}{/p}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'\n{p}{strong}{/strong}{br}\n{strong}{/strong}{br}\n{strong}{/strong}{br}\n{strong}{/strong}{br}\n{strong}{/strong}{br}\n{strong}{/strong}{br}\n{strong}{/strong}{br}\n{strong}{/strong}{/p}\n', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}READ MORE:.*?{/strong}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{li}\s*{/li}', "", clean_text, flags=re.DOTALL)

    # For foxsanantonio.com
    clean_text = re.sub(r'{p}{strong}RELATED.*?{/strong}{/p}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}ALSO\| \{/strong}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}ALSO \| \{/strong}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}  to learn more about SAMMinistries.*{/p}', "", clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}If you think you&#8217;re owed money from a former employer click {/p}', "", clean_text, flags=re.DOTALL)

    # For news4jax.com
    clean_text = re.sub(r'} Visit the Jacksonville Icemen Warriors website:  jacksonvilleicemenwarriors.com  to learn how to join the team.{', '}{', clean_text, flags=re.DOTALL)

    # For news.wfsu.org
    clean_text = re.sub(r'{b}Updated.*?(?:AM|PM) ET{/b}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r"""(}[\s]*Loading...[\s]*{)""", '}{', clean_text, flags=re.DOTALL)

    # For news4sanantonio.com
    clean_text = re.sub(r'{p}  for more rodeo info. {/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}  for more information. {/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\^ Not a Live Nation Date{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub('}\* With Billy Joel{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub('}\+ Festival Date{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Also\: \{strong}{/strong}{br}{/p}', '', clean_text, flags=re.DOTALL)

    # For abc7news.com
    clean_text = re.sub(r'} Watch the event live when it happens on the  ABC7 app  or wherever you stream.{', '}{' , clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}  RELATED:.*?{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}  MORE:.*?{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'} See the  full complaint here .{', '}{' , clean_text, flags=re.DOTALL)
    clean_text = re.sub(r"} We'll be streaming live coverage of the 49ers ahead of the Super Bowl in the video player above, on the  ABC7 News app , or by  downloading the ABC7 Bay Area App to watch on Roku, Amazon Fire, Apple and Google TV. {", '}{', clean_text, flags=re.DOTALL)

    clean_text = re.sub(r'How to watch ABC7 News coverage live', '', clean_text, flags=re.DOTALL)

    clean_text = re.sub(r'}\s*\$\d+(\.\d+)?\s*{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}     Valid:.*?{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}   Shop Now{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}   RELATED 49ERS/{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}  ALSO READ \|.*?{/b}{','}{', clean_text, flags=re.DOTALL)

    # goal.com
    clean_text = re.sub(r'} Article continues below{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{h2}Related links{/h2}', '', clean_text, flags=re.DOTALL)

    # pagesix.com
    clean_text = re.sub(r'{p}Click to share on Twitter.*?{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Click to share on Facebook.*?{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'Page Six may be compensated and/or receive an affiliate commission if you buy through our links.', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\n+\s*Follow Page Six&#8217;s coverage of Super Bowl 2024\s*{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\n+\s*{/p}\n\s*Want more celebrity and pop culture news\?\s*{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\n\s*Start your day with Page Six Daily\.\s*{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\n\s*\t*\s*Thanks for signing up!\s*\t*\s*{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\n\t*\n*\s*Enter your email address\s*{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\n*\s*Please provide a valid email address\.\s*{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\n\s*By clicking above you agree to the\s*Terms of Use\s*and\s*Privacy Policy\s*\.\s*{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\n\s*Want celebrity news as it breaks\? Hooked on Housewives\?\s*{/p}\n\s*{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}Check out more newsletters{', '}{', clean_text, flags=re.DOTALL)

    # For kob.com
    clean_text = re.sub(r'{p}Watch the video above for more.{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}For Related Stories:{/strong}','', clean_text, flags=re.DOTALL)

     # For ypradio.org
    clean_text = re.sub(r'{p}For a list of what is allowed and what is prohibited in carry-ons and checked luggage visit.*?{/p}','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{b}Updated.*?(?:AM|PM) ET{/b}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}This article was originally published on  WBUR.org.  \n{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p} can be found here  \n{/p}','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r"""(}[\s]*Loading...[\s]*{)""", '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub("""\n Copyright 2024  Boise State Public Radio News {/p}\n""",'', clean_text, flags=re.DOTALL)

    # For fox5atlanta.com
    clean_text =re.sub('article{/p}','', clean_text, flags=re.DOTALL)
    clean_text =re.sub('{p}Find the latest Weather Alert messages  here .{/p}','', clean_text, flags=re.DOTALL)
    clean_text =re.sub('{p}The FOX 5 Storm Team will continue to keep you up to date on the latest changes. Watch the most current forecast on FOX 5 Atlanta, streaming on FOX5Atlanta.com and on FOX Local for your Smart TV.&#160;{/p}','',clean_text, flags=re.DOTALL)
    clean_text =re.sub('{strong}&#160;AND FOLLOWING&#160;{/strong}','', clean_text, flags=re.DOTALL)
    clean_text =re.sub('{p}{strong}We will continue to follow the latest on this breaking news story. Stay tuned to FOX 26 and FOX26Houston.com for the very latest.{/strong}{/p}','', clean_text, flags=re.DOTALL)
    clean_text =re.sub('{p}Image 1 of 7{/p}','', clean_text, flags=re.DOTALL)
    clean_text =re.sub('{p}Image 1 of 25{/p}','', clean_text, flags=re.DOTALL)



    # display(clean_text)
#########################################################
   

    # For fox5sandiego.com
    clean_text = re.sub(r'The Associated Press contributed to this report.', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'\{p\}\(ProVideo contributed to this report.\)\{/p\}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Updated.*?(?:[aApP]\.?[mM]\.?|AM|PM)\s*ET{/p}', '', clean_text, flags=re.DOTALL)

    # For fox7austin.com (continues.....)
    clean_text = re.sub(r'{p}Image \d+ of \d+{/p}  &#9660;{/p}{p}[^{]*{/p}', '', clean_text, flags=re.DOTALL)
    
    #For fox32chicago.com
    clean_text = re.sub(r'{p}To explore the offerings and learn more about the participating restaurants, visit  ChiBlackRestaurantWeek.com .{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}{strong}DONATE: {/strong}{strong}.*?{/strong}{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Case in point:  the Super Bowl .{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*Related\s*{', '}{', clean_text,  flags=re.DOTALL)
    clean_text = re.sub(r'{strong}READ MORE:{/strong}{strong}.*?{/strong}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}LINK: {/strong}{strong}.*?{/strong}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'\{strong\}&#8217;EASTER\?\{/strong\}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}{i}{strong}LINK: {/strong}{/i}{i}{strong}.*?{/i}{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}RELATED:.*?{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Image (\d+) of (\d+){/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong} The criminal history of Moreno is linked below to a PDF:{/strong}', '', clean_text, flags=re.DOTALL) 
    clean_text = re.sub(r'FOX 26&#160;Houston&#160;is now on the FOX LOCAL app available through Apple TV, Amazon FireTV, Roku and Google Android TV', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*Featured\s*{', '}{', clean_text, flags=re.DOTALL)

    # For fox10phoneix.com
    clean_text = re.sub(r'{p}If you&#8217;re struggling with high-interest debt you want to pay off ASAP, just  plug in some simple information into Credible\'s free online tool to determine if a debt consolidation loan is your best option .{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'\{p\}\{strong\}Have a finance-related question, but don\'t know who to ask\? {/strong\}{/p\}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}No more information was made available.{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}Map of where Pyramid Trail is in Sedona:{/strong}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'\({strong}\{/strong}\)\{/p\}\{/p\}{h2}Map of where the crash happened{/h2}{p}&#160;{/p}\{/p\}', '', clean_text, flags=re.DOTALL)

    # For oregonlive.com
    clean_text = re.sub(r'{b}MORE DUCKS COVERAGE{/b}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'''{p} \n\n{i}{b} A roundup of conversations we're having daily on the site. {/b} Subscribe to the Reckon Daily for stories centering marginalized communities and speaking to the under-covered issues of the moment.{/i}{/p}''', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}{b}Read more: {/b}.*?{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'} Have a burning question\? Send me an email at\s+or tweet\s+! Or, if you want to ask me a question with total anonymity,\s+use this Google form\s+\.{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'''\{b\}Read and listen to more Why Tho\? here\.\{/b\}''', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'This story originally appeared on Underscore.news ', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'\{b\}A weekly newsletter for the chronically online and easily entertained\. \{\/b\} Honey dishes us savvy analysis on culture, entertainment and power to make you the group chat MVP\. Subscribe today! \{\/i\}\{\/p\}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'\{b\}\(The 2024 season of &#8220;Little People, Big World&#8221; premieres at 9 p\.m\. Tuesday, Feb\. 20 on TLC\. The show can be \{\/b\}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{b}streamed on Fubo{/b}{b}{/b}{b}Sling TV {/b}{b}{/b}{b}Max.{/b}{b}\)', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{b}More of our coverage:{/b}{/p}{/p}{/p}{b}.*?{/b}', '', clean_text, flags=re.DOTALL)

    # For foxnews.com (continue.....)
    clean_text = re.sub(r'Join Fox News for access to this content', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'Plus get unlimited access to thousands of articles, videos and more with your free account!', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Please enter a valid email address.{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}By entering your email, you are agreeing to Fox News  Terms of Service  and  Privacy Policy  , which includes our  Notice of Financial Incentive  . To access the content, check your email and follow the instructions provided.{/p}', '', clean_text, flags=re.DOTALL)

    # For indiatimes.com (continues.....)
    clean_text = re.sub(r'{b}Where To {/b}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}For more news and updates&#160;from the world of&#160;&#160; OTT , and&#160; celebrities &#160;from&#160; Bollywood &#160;and&#160; Hollywood , keep reading&#160; Indiatimes Entertainment .{/strong}', '', clean_text, flags=re.DOTALL)

    # For independent.co.uk (continues.....)
    clean_text = re.sub(r'{p}Access unlimited streaming of movies and TV shows with Amazon Prime Video{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Sign up now for a 30-day free trial{/p} Sign up {img src={IMG_\d+}}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}{p}Sign up now for a 30-day free trial{/p} Sign up  {', '}{', clean_text, flags=re.DOTALL)

    # For stltoday.com
    clean_text = re.sub(r'}\s*Get email notifications on {{subject}} daily!{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*Your notification has been saved.\s*{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*There was a problem saving your notification.\s*{/p}\s*{{description}}{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}Email notifications are only sent once a day, and only if there are new matching items.{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*Manage followed notifications\s*\s*Followed notifications{/h4}\s*{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'\{h4\}Please log in to use this feature\{/h4\}\s*Log In', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'\{strong\}Don\'t have an account\?\{/strong\}\s*Sign Up Today', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*Catch the latest in Opinion{/h2}\s*Get opinion pieces, letters and editorials sent directly to your inbox weekly!{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}Listen now and subscribe:  Apple Podcasts  \|  Spotify {/strong}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*The business news you need{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*Get the latest local business news delivered FREE to your inbox weekly.{', '}{', clean_text, flags=re.DOTALL)

    # For pantagraph.com
    clean_text = re.sub(r'{strong}Mark&#160;Sperry,&#160;Normal{/strong}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Check out our roundup of the latest special events, music, theater, nightlife and kids events.{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}To submit an item, send an email to aph.com. {/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{h4} How Time Flies is a daily feature looking back at Pantagraph archives to revisit what was happening in our community and region.&#160;{/p}{/h4}', '', clean_text, flags=re.DOTALL)

    # For myhighplains.com
    clean_text = re.sub(r'{strong}More stats from Kot at Fort Lewis College include:{/strong}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}For the latest  Amarillo news  and regional updates, check with  MyHighPlains.com  and tune in to KAMR Local 4 News at 5:00, 6:00, and 10:00 p.m. and Fox 14 News at 9:00 p.m. CST.{/strong}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}To read Cowles&#\d+; entire story on The Cut,&#\d+;.{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Watch the full press conference at UCCS in the video player above.{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}This segment is sponsored by For the Duration Homes.{/p}', '', clean_text, flags=re.DOTALL)

   # For nbcdfw.com (continues.....)
    clean_text = re.sub(r'{strong}Get DFW local news, weather forecasts and entertainment stories to your inbox.  &#160;newsletters . {/strong}', '', clean_text, flags=re.DOTALL)

    # For tucson.com
    clean_text = re.sub(r'{p}Howard Fischer is a veteran journalist who has been reporting since 1970 and covering state politics and the Legislature since 1982. Follow him on X, formerly known as Twitter, and Threads at or&#160;email&#160; .&#160;{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}{i}{strong} Subscribe to stay connected to Tucson. {/strong} A  subscription  helps you access more of the local stories that keep you connected to the community.{/i}{br}{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Disclaimer: As submitted to the Arizona Daily Star.{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Register for more free articles.{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\n\s*Log in\s*\n\s*Sign up\s*\n\s*\n\s*{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Respond:   Write a letter to the editor  \|  Write a guest opinion {/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}The following is the opinion and analysis of the writer:{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\n\n\n\n Want to see more like this\?\{/h2\}\n\s+Get our local education coverage delivered directly to your inbox.{', '}{', clean_text, flags=re.DOTALL)

    # For killeenpdnews_com
    clean_text = re.sub(r'}\n Share this:{/h3}{','}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\n\n\n\n ###{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}   Like this:{', '}{', clean_text, flags=re.DOTALL)

    # For cbsaustin.com
    clean_text = re.sub(r'{p}{strong}Editor|\'s Note: {/strong}.*?{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong} (\w+) (\w+) on X at for the latest trending national news. Have a news tip\? Send it to', '{/strong}', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}See also: {/strong}{/p}{p}.*?{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r"{p}Anyone with information regarding Vue\'s whereabouts is asked to call \(\d+\) \d+\-\d+.", '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}{strong}PREVIOUS COVERAGE \| {/strong}.*?{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}READ MORE \| {/strong}.*?{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p} (\w+) (\w+) on X at for the latest trending national news. Have a news tip\? Send it to.', '{/p}', clean_text, flags=re.DOTALL)

    # For nbcnews.com (continues.....)
    clean_text = re.sub(r'} Katlyn Butler{/p}{/p} Video shows Texas firefighters driving along highway surrounded by wildfire {/h2}{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'} Video showed firefighters from the Greenville Fire Department driving through wildfires raging across a highway in the Texas Panhandle.{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'} via tfswildfires.com{', '}{', clean_text, flags=re.DOTALL)

    # For newsweek.com (continues.....)
    clean_text = re.sub(r'{strong}Do you have funny and adorable videos or pictures of your pet you want to share\? Send them to with some details about your best friend and they could appear in our Pet of the Week lineup.{/strong}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{h2}Uncommon Knowledge{/h2}','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'Newsweek is committed to challenging conventional wisdom and finding connections in the search for common ground.', '', clean_text, flags=re.DOTALL)

    # For cbs12.com
    clean_text = re.sub(r'{strong}See also: {/strong}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}RELATED  \| {/strong}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}SEE ALSO \| {/strong}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}MORE ON NEWS \d+ \| {/strong}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r"{p}Click on the video link to watch Tagovailoa play at the Pro-Am, and to watch his interview, where he discusses the movie \'Happy Gilmore\', and his motivation on the golf course.{br}{/p}", '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}Have something for the   team to investigate\? Call or text the national tip line at 202-417-7273.{/strong}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{strong}See Also:{/strong}', '', clean_text, flags=re.DOTALL)

    # For theblaze.com
    clean_text = re.sub(r'Like Blaze News\? Bypass the censors, sign up for our newsletters, and get stories like this direct to your inbox.  Sign up here !', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'Like Blaze News\? Bypass the censors, sign up for our newsletters, and get stories like this direct to your inbox. Sign up here!', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{h2}Want more from Sara Gonzales\?{/h2}', '' , clean_text, flags=re.DOTALL)
    clean_text = re.sub(r"{p}To enjoy more of Sara's no-holds-barred take to news and culture,  subscribe to BlazeTV  &#8212; the largest multi-platform network of voices who love America, defend the Constitution, and live the American dream.{/p}", '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}\n\tTo hear more, watch the clip below.\n{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{h2}Want more from Glenn Beck\?{/h2}', '' , clean_text, flags=re.DOTALL)
    clean_text = re.sub(r"{p}To enjoy more of Glenn&#8217;s masterful storytelling, thought-provoking analysis, and uncanny ability to make sense of the chaos,  subscribe to BlazeTV  &#8212; the largest multi-platform network of voices who love America, defend the Constitution, and live the American dream.{/p}", '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r"{h2}Here\'s more on the SCOTUS announcement: {/h2}", '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r"{h2}Here\'s a local news report about the incident:{/h2}", '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r"{h2}\n\tHere\'s a news report about the attack:\n{/h2}", '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r"{h2}Here\'s a news report about the incident:{/h2}", '', clean_text, flags=re.DOTALL)

    # For bangordailynews.com
    clean_text =re.sub('''Letters submitted by BDN readers are verified by BDN Opinion Page staff. Send your letters to&#160; {/p}''','', clean_text, flags=re.DOTALL)
    clean_text =re.sub('More articles from the BDN{/h3}','', clean_text, flags=re.DOTALL)
    clean_text =re.sub('{p}This article appears through a media partnership with  Maine Public .{/p}','', clean_text, flags=re.DOTALL)
    clean_text =re.sub('The BDN Editorial Board operates independently from the newsroom, and does not set policies or contribute to reporting or editing articles elsewhere in the newspaper or on&#160; bangordailynews.com .{/p}','', clean_text, flags=re.DOTALL)
    clean_text =re.sub('The BDN Opinion section operates independently and does not set news policies or contribute to reporting or editing articles elsewhere in the newspaper or on&#160; bangordailynews.com .{/p}','', clean_text, flags=re.DOTALL)
    
    # For binghamtonhomepage.com
    clean_text = re.sub(r'{p}Updated.*?(?:[aApP]\.?[mM]\.?|AM|PM)\s*ET{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Updated at \d+:\d+ [aApP]\.?[mM]\.?{/p}', '', clean_text, flags=re.DOTALL)
    
    # For indiatimes.com (continues.....)
    clean_text = re.sub("""(}{strong}*For more trending stories, follow us on {/strong}*{)""",'}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub('}For the latest and more interesting financial news, keep reading Indiatimes Worth.&#160; {', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub('}For more informative articles on historical and upcoming events from around the world, please visit  Indiatimes Events .&#160;{','}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub('}For more stories like these, follow us on&#160; Indiatimes Lifestyle.&#160; {','}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub('}For more informative articles on historical and upcoming events from around the world, please visit&#160; Indiatimes Events .{','}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub('}For more news and current affairs from around the world, please visit&#160;{','}{', clean_text, flags=re.DOTALL )
    clean_text = re.sub('}Indiatimes News.{','}{', clean_text, flags=re.DOTALL)
    
    # For allrecipes.com
    clean_text = re.sub(r'}\n    Related Content: {', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*{strong}Get the Recipe:{/strong}.*?{', '}{', clean_text, flags=re.DOTALL)
    
    # For wfmz.com
    clean_text = re.sub(r'}For questions or concerns, please contact them directly at                                \n                                \n                                {','}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}For the latest Blue Moo updates, follow the business&#8217;  Facebook page .{','}{', clean_text, flags=re.DOTALL)
    
    # For dallasinnovates.com
    clean_text = re.sub(r'{h2}Get on the list.{br}\nDallas Innovates, every day.{/h2}','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'&#8217;s new and next in Dallas-Fort Worth, every day.{/p}','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p} Go here for more information .{/p}','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Read more  in our story here .&#160;{/p}','', clean_text, flags=re.DOTALL)
    
    # For madison.com
    clean_text = re.sub(r'}\s*Your notification has been saved.\s*{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*There was a problem saving your notification.\s*{/p}\s*{{description}}{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}Email notifications are only sent once a day, and only if there are new matching items.{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*Manage followed notifications\s*\s*Followed notifications{/h4}\s*{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'\{h4\}Please log in to use this feature\{/h4\}\s*Log In', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'\{strong\}Don\'t have an account\?\{/strong\}\s*Sign Up Today', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*The business news you need{', '}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*Get the latest local business news delivered FREE to your inbox weekly.{','}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*Get email notifications on {{subject}} daily!{','}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*0{/strong} comments\s*{','}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'Want to see more like this\?\{\/h2}.*?Get our local education coverage delivered directly to your inbox\.{\/p}','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*Catch the latest in Opinion{','}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*Get opinion pieces, letters and editorials sent directly to your inbox weekly!{','}{', clean_text, flags=re.DOTALL)
    
    # For texasmonthly.com
    clean_text = re.sub(r'}\s*Popular Videos\s*{','}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\n more \n {','}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'} \n More About:{','}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}This article originally appeared in the March 2024 issue of&#160;Texas Monthly with the headline.*? {strong}Subscribe today{/strong}{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}This article originally appeared in the March 2024 issue of Texas Monthly with the headline.*? {strong}Subscribe today{/strong}{/p}', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}This article originally appeared in the March 2024 issue of&#160;Texas Monthly.&#160; {strong}Subscribe today{/strong}{/p}','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}This article originally appeared in the March 2024 issue of&#160;Texas Monthly&#160;with the headline &#8220;.*?&#8221;&#160; {strong}Subscribe today{/strong}{/p}','', clean_text, flags=re.DOTALL)
    
    # For pasadenanow.com
    clean_text = re.sub(r'{p}Get all the latest Pasadena news, more than \d+ fresh stories daily, \d+ (?:days|Days) a week at \d+ (?:[aApP]\.?[mM]\.?|AM|PM){/p}','', clean_text, flags=re.DOTALL)

    # For easternnewmexiconews.com
    clean_text = re.sub(r'{p}&#8212; Please email the publisher:','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'Contact her','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Questions on the risks of PFAs exposure may be sent to .{/p}','', clean_text, flags=re.DOTALL)
    
    # For nottinghammd.com
    clean_text = re.sub(r'{p}View a full list of the  recalled model numbers online here .{/p}','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}The full report can be viewed  online here at WalletHub .{/p}','',clean_text, flags=re.DOTALL)
    
    # For kztv10.com
    clean_text = re.sub(r'{p}{b}Trending stories at  Scrippsnews.com {/b}{/p}','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}Scripps News has confirmed a vote on short-term funding is expected on Thursday in the House of Representatives.{/p}','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}{b}iden, Trump projected to win primaries in Michigan {/b}{/p}','', clean_text)
    clean_text = re.sub(r'} originally appeared on  Simplemost.com {','}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p} KRIS 6 News App. {/p}','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}To donate or for more information on the American Legion Post 405 call 361-701-1862 or send an email at the latest local news updates, {/i} KRIS 6 News App. {/p} ','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}Key ingredients: {','}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}\s*KRIS 6 NEWS{','}{', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p} making a tax-deductible gift today {/p}','', clean_text, flags=re.DOTALL)
    
    # For kristv.com
    clean_text = re.sub(r'{p}&#160;for the full travel advisory.{/p}','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'}MORE:  7 ways to keep your rugs clean when you have pets {','}{', clean_text, flags=re.DOTALL)

    # For keranews.org
    clean_text = re.sub(r'{p}This  article  first appeared on  Fort Worth Report  and is republished here under a Creative Commons license.{/p}','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p}The News{/p}','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p} making a tax-deductible gift {/p}','', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'{p} making a tax-deductible gift today. {/p}','', clean_text, flags=re.DOTALL)
    
    # For click2houston (continue.....)
    clean_text = re.sub(r'} Recommended Videos{','}{', clean_text, flags=re.DOTALL)



    # display(clean_text)


    clean_text = re.sub('(\\n)','',clean_text) #removing new line character
    clean_text = re.sub('(\\t)','',clean_text) #removing tabular character
    clean_text = re.sub('(\\r)','',clean_text) #removing carriage return character
    clean_text = re.sub('({p}{br}{/p})','',clean_text) # removing line break
    clean_text = re.sub('({p}[\s]*{/p})','',clean_text) #removing empty p-tag keyword
    clean_text = re.sub('({strong}[\s]*{\/strong})','',clean_text) #removing empty strong-tag keyword
    clean_text = re.sub('({/a}[\s]*{/a})','',clean_text) #removing empty a-tag keyword



    clean_text = html.unescape(clean_text) #decoding unicode entities using html parser
    clean_text = replace_all1(clean_text,tags)

    # cleaning emoji
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                           "]+", flags=re.UNICODE)

    clean_text = emoji_pattern.sub(r'', clean_text)
    clean_text = unicodedata.normalize("NFKD",clean_text) #decoding utf-8 unicode data which is producing spacing

      # storing words in list with no extra spaces
    clean_text= [j for j in clean_text.strip().split(" ") if j !=""]
    clean_text = " ".join(clean_text)
    clean_text = fix_text(clean_text)
      # clean_text = clean_text.replace("â€TM", "'")

    block_src_list = re.findall(r'<blockquote src={BLOCK_.*?>', clean_text, flags=re.DOTALL)
    iframe_src_list = re.findall(r'<iframe src={IFRAME_.*?>', clean_text, flags=re.DOTALL)

    for l in range(0, len(block_src_list),1):
          clean_text = re.sub(block_src_list[l], blockquote_list[l], clean_text, flags=re.DOTALL)

    for k in range(0, len(iframe_src_list), 1):
          clean_text = re.sub(iframe_src_list[k], iframe_list[k], clean_text, flags=re.DOTALL)

    return clean_text

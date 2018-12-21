# One-Click Demo for math test

### 這一個Demo主要是說明如何在git上做一個one-click就可以自動佈署到Heroku的line-bot專案按鈕
### 此Demo有對於MongoDB的操作範例，並實作出題式的line交談功能，用戶回答的問題會比較上一次出的題目，確認是否回答正確

- 可以按以下的按鈕進行自動佈署本App
- one-click button to auto deploy this demo

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)


### 說明如下
- 如下，要加入這一段，就可以產生按鈕，可以參考[這邊](https://devcenter.heroku.com/articles/heroku-button)


`[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)`


- 這一個App有幾個元素，是一個App最基本的三個檔案：
    - app.py: 主程式
    - Procfile: App類型，如何啟動
    - requirements.txt: 需要的套件
    
- 另外，在你的repo上根目錄下放一個 app.json 檔，格式如下，這邊多了「env」項目，裡面的「LINE_CHANNEL_SECRET」、「LINE_CHANNEL_ACCESS_TOKEN」是Line-bot API需要的東西，因此放環境變數讓佈署者填入，這樣就不用寫死在程式碼中：

<pre><code>{
    "name": "flask line-bot demo",
    "description": "a line-bot with math test function",
    "repository": "https://github.com/maloyang/one-click-line-math",
    "env": {
        "LINE_CHANNEL_SECRET": {
          "description": "Input your 'Channel secret'"
        },
        "LINE_CHANNEL_ACCESS_TOKEN": {
            "description": "Input your 'Channel access token'"
        }
    },
    "addons": [
        {
            "plan": "mongolab:sandbox"
        }        
    ]
}
</code></pre>

- 另外因為本line-bot會用到mongoDB，因此有加入一個mongolab的免費db來使用，安裝過程中，會自動裝好帶入

- 只要完成了以上的事，就可以做一個快速佈署按鈕分享你的專案給大家使用!!
- 以這一個demo為例，他會把你帶到heroku的畫面，假設你已經登入了，那動呈現的畫面如下

![line-bot-demo](https://imgur.com/V6UoAQY.png)

- 然後把你的app名稱、"LINE_CHANNEL_SECRET"、"LINE_CHANNEL_ACCESS_TOKEN" 就可以按"Deploy app"佈署囉!
- 當然以我這一個範例來說，你還需要在你的line develop channel的頁面上把你的heroku app的位址填進來，這樣line才知道要把訊息送到哪裡

![要填入callback的address](https://imgur.com/FPU4acI.png)


### one-click教學part1 請參考[這邊](https://github.com/maloyang/one-click-flask-hello)。
### one-click教學part3 請參考[這邊](https://github.com/maloyang/one-click-line-echo-db)。

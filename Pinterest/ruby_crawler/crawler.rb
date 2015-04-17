require 'nokogiri'
require 'json'
require 'open-uri'
# require 'execjs'

=begin
The crawl method in Base crawler will crawl all pinterest url in the source file
and write result list of pins into a json file.


Pins contains the following attributes:
	id: the number in the pin url address
    name: name of the pin
    image: image url
    source: source labeled by pinterest, which will be described below
    credit: some pin has credit values
    comments: list comments of the pin, which will be described below
    belonging board: the board that the pin bleongs to
    related pins: related pins that are suggested by pinterest

Source constins the source labeled by pinteres:
    title: the text title given by pinterest
    url: link to the source

comment contains comments from pinterest:
    creator: comment creator
    creator_url: link to the creator's page
    content: comment content
    content_src: the inner html of the content block. The purpose is to
                 maintain the links or other components in the comment
=end
class BaseCrawler
    def initialize(inputfile = 'Pinterest.csv', outputfile = 'output.json')
        @input = inputfile
        @output = outputfile
        @logfile = './'+Time.now.to_s+'_log.txt'
        @header_hash = { "User-Agent" => 
                "Mozilla/5.0 (Macintosh;"+
                " Intel Mac OS X 10_6_8)"+
                " AppleWebKit/536.11 (KHTML,"+
                " like Gecko) Chrome/20.0.11"+
                "32.57 Safari/536.11"}
        @pin_url = Regexp.new('\Ahttps?://(www\.)?pinterest\.com/pin/.*')
    end


    def crawl()
        pins = []
        boards = []
        f = File.open(@input, 'r')
        f.each_line do |l|
            url = l.partition('""expanded_url"":')[2]
            url = url.split('""')[1]
            begin
                if @pin_url.match(url)
                    pins << crawlPin(url)
                else
                    boards<< crawlBoard(url)
                end
            rescue
                File.write(@logfile, 
                           Time.now.to_s+': Error occured when crawling '+
                                         if url.nil? then "nil\n" else url+"\n" end, 
                           mode:'a')
            end
        end
        f.close
        File.write('pins.json', pins.to_json)
        File.write('boards.json', boards.to_json)
    end


    def crawlPin(url='http://pinterest.com/pin/355925176776424800/')
        begin
            html = Nokogiri::HTML(open(url, @header_hash))
        rescue
            url = url.sub! 'http', 'https'
            html = Nokogiri::HTML(open(url, @header_hash))
        end
        id = url.split('pin/')[1].sub! '/', ''
        id = id.to_i

        # major pin information
        doc = html.css('div[class="detailed PinBase Pin Module"]')[0]

        image = doc.css('div[class=pinImageSourceWrapper] div[class=imageContainer] img')[0]['src']
        name = doc.css('h2[itemprop=name]').text.strip
        sourceCont = doc.css('div[class=sourceFlagWrapper]')
        source = {'title'=>sourceCont.text.strip, 'src'=>sourceCont.css('a')[0]['href']}

        tmp = doc.css('div[class=pinCredits]')
        pinCredit = {}
        begin
        	pinCredit['name'] = tmp.css('div[class=creditName]')[0].text.strip
        rescue
        	pinCredit['name'] = ''
        end
        begin
        	pinCredit['title'] = tmp.css('div[class=creditTitle]')[0].text.strip
        rescue
        	pinCredit['title'] = ''
        end
        begin
        	pinCredit['src'] = tmp.css('a')[0]['href']
        rescue
        	pinCredit['src'] = ''
        end

        commentsCont = doc.css('div[class=commenterNameCommentText]')
        comments = []
        commentsCont.each do |commentCont|
            creator = commentCont.css('div[class=commenterWrapper] a')[0]
            commentContent = commentCont.css('h1[class=commentDescriptionContent]')
            comments << {'creator'=>creator.text.strip,
                         'creator_url'=>creator['href'],
                         'content'=>commentContent.text.strip,
                         'content_src'=>commentContent.inner_html}
        end

        # pin board link
		doc = html.css("div[class='Module CloseupSidebar']")[0]

        belonging = doc.css("div[class=boardHeader]")
        belongingBoard = {}
        belongingBoard['title'] = belonging.css('h3[class=title]').text.strip
        belongingBoard['src'] = 'https://www.pinterest.com'+belonging.css('a')[0]['href'].strip


        # related pin information
        doc = html.css('div[class=closeupBottom]')[0]

        relatedPins = []
        relatedPinsCont = doc.css('div[class=relatedPinsWrapper]')[0]
        relatedPinsCont = relatedPinsCont.css('div[class=pinWrapper]')
        relatedPinsCont.each do |relatedPin|
        	relatedPins << relatedPin.css('div[class=pinHolder] a')[0]['href']
        end

        credit = 

        {'id'=>id, 'name'=>name, 'image'=>image, 'source'=>source, 'credit'=>pinCredit,
         'belonging board'=>belongingBoard, 'comments'=>comments, 
     	 'related pins'=>relatedPins}
    end

    def crawlBoard(url='https://www.pinterest.com/consciousgaze/main/')
        pin_urls = []
        begin
            doc = Nokogiri::HTML(open(url, @header_hash))
        rescue
            url = url.sub! 'http', 'https'
            doc = Nokogiri::HTML(open(url, @header_hash))
        end

        # gather board info
        boardName = doc.css('h1[class=boardName]').text.strip
        boardDesp = doc.css('p[class=description]').text.strip
        boardOwner = doc.css('h4[classs=fullname]').text.strip

        board = {'owner'=>boardOwner,
        		 'title'=>boardName,
        		 'description'=>boardDesp}

        pinCnt = 0
        pinsCont = doc.css("div[class=pinWrapper]")
        while pinCnt!=pinsCont.length do
            ExecJS.eval('window.scrollTo(0,document.body.scrollHeight)')
            pinCnt = pinsCont.length
            pinsCont = doc.css("div[class=pinWrapper]")
            puts pinCnt.to_s+" "+pinsCont.length.to_s
        end
        pinsCont.each do |pinCont|
            pin_urls << 'https://pinterest.com'+pinCont.css('div[class=pinHolder] a')[0]['href']
        end
        pin = []
        pin_urls.each do |url|
            pin << crawlPin(url)
        end
        board['pins'] = pin
        return board
    end
end


c = BaseCrawler.new('../pinterest_data.csv')
# File.write('./boards.json', c.crawlBoard('https://www.pinterest.com/clearcreekid/pet-supplies-pet-home-remedies/').to_json)
File.write('./pins.json', c.crawlPin.to_json)
# c.crawl

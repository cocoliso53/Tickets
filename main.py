import requests

def search(bgn_tag,mid_tag,end_tag,text,delta=0):
    #Basic funtion that looks for certain html tags and what's between them. 
    # Pretty much a substitute for bs4 
    result = []
    pos = 0

    while True:
        start = text.find(bgn_tag, pos)
        if start == -1:
            break
        
        mid = text.find(mid_tag, start) + delta
        end = text.find(end_tag,mid)
        info = text[mid+1:end]
        result.append(info)
        pos = end
    
    return result


def ticket():
    #Makes a basic get request from a website to get info of some events.
    # Uses the previous functions to get the event, venue and date
    # returns a list for each one of those
    session = requests.Session()
    url = "https://www.ticketweb.com/search?q="
    get_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
               "Accept-Encoding": "gzip, deflate, br",
               "accept-language": "en-US,en;q=0.9,es-419;q=0.8,es;q=0.7",}
               
               
    main_html = session.get(url,headers=get_headers,verify=False)
    resp  = main_html.content.decode()
    
    # Event tag
    bgn_tag = '<a class="main-info theme-title theme-mod-bg mttext-ellipsis mttext-ellipsis-2" ng-if="onPhone">'
    # venue tag
    bgn_tag_venue =  '<a class="main-info theme-primary-color ellipsis visible-xs"'
    
    # useful for both event and venues
    mid_tag =  '>'
    end_tag = '</a>'

    # dates tags
    bgn_tag_date = '<small class="sub-info theme-subTitle"'
    mid_tag_date = 'data-ng-if="onPhone">'
    end_tag_date = '</small>'

    events = search(bgn_tag=bgn_tag,mid_tag=mid_tag,end_tag=end_tag,text=resp)
    venues = search(bgn_tag=bgn_tag_venue,mid_tag=mid_tag,end_tag=end_tag,text=resp)
    dates = search(bgn_tag=bgn_tag_date,mid_tag=mid_tag_date,end_tag=end_tag_date,text=resp,delta=len(mid_tag_date))


    return events,venues,dates

def etix():
    session = requests.Session()
    etix_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9,es-419;q=0.8,es;q=0.7",
                "Connection": "keep-alive"}


    payload = {"current_selection_method": "byBest",
                "3025922": "2",
                "isAdjacent": "no",
                "addSeatBtn": ""}
    url = "https://www.etix.com/ticket/p/6418771"
    
    post_url = "https://www.etix.com/ticket/online/performanceSale.do?method=addSeat"

    # Creates a session so we can have a jsessionid
    first = session.get(url=url,headers=etix_headers)

    # makes the actual selection of tickets

    #NOTE I has succes with avoiding the fist get to get a sessionid
    # By sending a post request to the url: "https://www.etix.com/ticket/online/performanceSale.do;jsessionid=3952ABD532A3C25EB3EC7E4644455524?method=addSeat"
    # and changing the jsessionid a little bit, but that would require some other libraries like random, but then gain maybe I
    # took the instructions quite literal 
    post_response = session.post(url=post_url,data=payload)


    return post_response.text

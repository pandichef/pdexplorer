import pandas as pd
import numpy as np

df1 = pd.DataFrame(
    {
        "rate": [5, 4.5, 4, 3.5, 3],
        "origfixedterm": [60, 84, 120, 180, 360],
        "origterm": [360, 360, 360, 180, 360],
        "origltv": [50, 60, 70, 80, 90],
        "origfico": [620, 640, 660, 680, 700],
        "age": [12, 12, 12, 12, 12],
        "origupb": [100, 200, 300, 400, 500],
        "upb": [100, 200, 300, 400, 500],
    }
)

yelp_reviews = [
    {
        "label": 4,
        "text": "Food was very good, loved the guacamole dip, not a huge fan of the salsa for the chips.   Salsa is a bit peppery.    Really enjoyed the food though, this place just opened early August, 2011.   I will be back for sure, very friendly staff, not the greatest looking place but not bad.",
    },
    {
        "label": 1,
        "text": "This place is tucked away in between a busy Starbucks and a large grocery store, among other small mom and pop shops. I needed a quick bite to eat and didn't want to deal with the line at Starbucks so I decided to pay a visit.\\n\\nThere's a huge poster in the entrance that advertises their $3 special for bagel with cream cheese and coffee. Bingo! I made my way in to divulge in their special. The dining area isn't anything extravagant, it's just what you need with lots of tables and chairs. Walking up to the order stand, I was quite disappointed to see that three-fourths of their bagel selection wasn't available. It was 10:50 AM so I wasn't sure that they just sold out of everything earlier in the morning or if they don't offer a large selection as listed. I opted for a simple blueberry bagel with cream cheese. \\n\\nUnlike Einstein Brothers where you can see the preparation of your food, this place has a huge wall from the order stand to the cashier's stand so preparation isn't visible. Whatever, I figure you can't mess up a bagel with cream cheese. They toasted my bagel (I didn't ask for this but I think I'd be annoyed if I didn't want it toasted) so that it had a nice crunch. But the bagel had absolutely no flavor. Blueberries? Nah, this bagel had me scratching my head wondering where the blueberry good ran off to.\\n\\nThey serve regular coffee as well as vanilla flavored coffee. Their vanilla coffee was pretty good, can't complain about that. \\n\\nAs the name states, this place serves gyros and deli sandwiches. Their \\\"New York\\\" bagels didn't impress me so I'm not sure if I'll be back anytime soon to try other items on their menu.  Sad face.",
    },
    {"label": 4, "text": "Great place, great service and friendly people"},
    {
        "label": 1,
        "text": "After the UYE @ Herbs and Rye was over there was talk of tacos, the crew all ended up going to another destination, but since I'm lazy I figured I'd check out the place 10 feet from my parked car.\\n\\nThe place is nothing more than a tiny shack with a big light up screen on top of it, they have menus on both sides of the windows, one in english and one in spanish. \\n\\nThey don't have a ton of variety, but everything is hand made, the tortillas are hand made, and mine were made to order.\\n\\nThe place wasn't really busy, which concerned me a little, but I thought I'd give it a try.\\n\\nI ordered a Carne Asada Taco and a Taco Al Pastor. I was a little surprised when I got my order, all there was on my plate was 2 tortillas with some meat on them, no lettuce, no cheese, nothing.\\n\\nThey do have a small toppings bar next to the window that had 2 salsas and a guac sauce, limes, cabbage, and jalapenos, on it, but I'm not really a fan of any of them.\\n\\nI squeezed some lime on to my meaty tortillas and gave them a try.\\n\\nThe Taco Al Pastor was pretty solid, the pork was cooked and seasoned well, but it was nothing special.\\n\\nThe Carne Asada Taco was rather disappointing, the beef was chewy and barely seasoned.\\n\\nThe tortillas were fresh and tasted pretty good, but I have to admit for $1.75 each I was expecting more than meat and a tortilla.\\n\\nThe only things saving this place from a 1 star review are the fact that the ladies were friendly, the food came out quick, and the al pastor was decent.\\n\\nIt will do in a pinch, but there are 3 other taco places within a block, so I'd say check them out first.\\n\\nOh and there are no tables or chairs or anywhere to sit, I had to sit in my car and eat my tacos",
    },
    {
        "label": 0,
        "text": "I agree with Insider Pages, the staff is super rude for either dine-in or to-go, I guess I am not pretty enough or the right color. Beware of cashier 19. \\nThe manager is controlled by the staff. In this economy with those prices and that attitude: NO THANK YOU! Never again. \\nTry DaVinci Pizza down the road, the owner takes pride in his pizza and the taste is almost as good for half the price.",
    },
    {
        "label": 0,
        "text": "I have NEVER written a review on ANYTHING, but I absolutely had to for this restaurant. I cooked Chinese food for years and preparing this food in such a bland way is hard to do, so bravo guys. I've ate here a few times and it's either ok or just plain not good, and I mean not good to the point where I will literally just toss it out rather than eat it. So take my review for what it is. I know the business and one review is not gonna make or break a restaurant, but they have definitely lost my family, friends and I as customers.",
    },
    {
        "label": 0,
        "text": "I love cafe rio but this location was very disappointing. The staff was very rude and the salad that I ordered comes with cheese but the guy only gave me a pinch and told me if I wanted more than that it would cost $1 more. The other locations give you cheese and don't argue with their customers over it. Then I asked for limes and they gave me lemons instead and when I told then, he rolled his eyes at me, like really. This location is very stingy with their ingredients and the staff have poor attitudes. I Will NEVER be back to this location EVER again and I have advised several others to go to a different location so they don't go through the same hassle I did. Lack of customer service is prevalent here.\\nFYI: If you hate your job that much that you treat your customers like shit, then quit your job. Management shouldn't allow this to happen, PERIOD!!!!!!!",
    },
    {
        "label": 1,
        "text": "My husband and I went to the Cheesecake Factory for lunch. PROS- no wait, friendly waiter, large menu. CONS- atmosphere was very warehouse/industrial, food was overpriced. We will not be going back.",
    },
    {
        "label": 3,
        "text": "Bartender was knowledgeable, friendly and knew how to make my favorite drink (a boulevardier) without having to look it up.  Upon ordering my second one, I made a suggestion as to how he could improve it (more compari) and he did as told and the second drink was even better.\\n\\nI ordered the pig ears for curiosity's sake.  The texture was slightly off-putting (the portion size was too big), but they were well seasoned and the salsa that came with it was very delicious.",
    },
    {
        "label": 2,
        "text": "This place certainly isn't new and fancy like many of the other locations on the strip, but it is an okay place to get a good night's rest. There were a lot of children running around and things were a bit dingy and run down, but the price is pretty awesome. Do beware of the additional resort fees, which do get you a coupon book with some decent stuff like a free premium ride at the adventure dome and 2 midway games, plus some deals on drinking and gambling. Resort fee also covered free wifi. There is a gym which was much nicer than I expected, but very difficult to find. Many people asked seem to not know where it was hidden and there are no helpful signs. I would suggest it be kept open 24 hours a day since this is the city that never sleeps, but the hours started early and ended semi late. The pool didn't appear to be anything worth checking out unless you are super hot, especially if you have used any of the other pools on the strip. We did have a problem with an alarm clock next door going off in the middle of the night, but staff did get it taken care of eventually. I also had a problem with my safe, which may have been forgetting my own code, and was impressed when security arrived prior to the maintenance man to verify my identification. Do beware the food at the buffet is not really edible. Overall I would stay here again, but mostly if I was with children or had a strange love for the free circus acts.",
    },
    {
        "label": 3,
        "text": "One of the best massages I have had. Ive gone to manu 5 star resorts yet I still think Seth's massage is just as good as many of them -- yet at a fraction of the cost.\\n\\nBeware however that this is not a 5 star spa experience! Its a small office with tiny massage rooms and VERY thin walls so you can hear people talking, which is annoying.  The thin walls are a big downside to this place. However, Seth seems to understands these limitations so is willing to give discounts and great deals for his massages which makes me ignore the thin walls\\n\\nIf you like deep tissue,  and are willing to deal with a non-chain small biz massage office, dont want to pay alot for a massage. Btw, Seth is a biz owner and a great masseuse so he books fast and it will take a day or two to call you back. Be patient though!  I highly recommend Seth for a great deep tissue massage!!",
    },
    {
        "label": 0,
        "text": "HORRIBLE! Got a manicure and polish started chipping after just a few hours! The worker that did manicure seemed uninterested and annoyed to be there while rushing through manicure. Overall poor experience. Will never go back",
    },
]

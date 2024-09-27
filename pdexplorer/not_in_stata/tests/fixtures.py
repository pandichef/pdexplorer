import pandas as pd
import numpy as np

# df1 = pd.DataFrame(
#     {
#         "rate": [5, 4.5, 4, 3.5, 3],
#         "origfixedterm": [60, 84, 120, 180, 360],
#         "origterm": [360, 360, 360, 180, 360],
#         "origltv": [50, 60, 70, 80, 90],
#         "origfico": [620, 640, 660, 680, 700],
#         "age": [12, 12, 12, 12, 12],
#         "origupb": [100, 200, 300, 400, 500],
#         "upb": [100, 200, 300, 400, 500],
#     }
# )

yelp_reviews = [
    {
        "stars": 4,
        "text": "Food was very good, loved the guacamole dip, not a huge fan of the salsa for the chips.   Salsa is a bit peppery.    Really enjoyed the food though, this place just opened early August, 2011.   I will be back for sure, very friendly staff, not the greatest looking place but not bad.",
    },
    {
        "stars": 1,
        "text": "This place is tucked away in between a busy Starbucks and a large grocery store, among other small mom and pop shops. I needed a quick bite to eat and didn't want to deal with the line at Starbucks so I decided to pay a visit.\\n\\nThere's a huge poster in the entrance that advertises their $3 special for bagel with cream cheese and coffee. Bingo! I made my way in to divulge in their special. The dining area isn't anything extravagant, it's just what you need with lots of tables and chairs. Walking up to the order stand, I was quite disappointed to see that three-fourths of their bagel selection wasn't available. It was 10:50 AM so I wasn't sure that they just sold out of everything earlier in the morning or if they don't offer a large selection as listed. I opted for a simple blueberry bagel with cream cheese. \\n\\nUnlike Einstein Brothers where you can see the preparation of your food, this place has a huge wall from the order stand to the cashier's stand so preparation isn't visible. Whatever, I figure you can't mess up a bagel with cream cheese. They toasted my bagel (I didn't ask for this but I think I'd be annoyed if I didn't want it toasted) so that it had a nice crunch. But the bagel had absolutely no flavor. Blueberries? Nah, this bagel had me scratching my head wondering where the blueberry good ran off to.\\n\\nThey serve regular coffee as well as vanilla flavored coffee. Their vanilla coffee was pretty good, can't complain about that. \\n\\nAs the name states, this place serves gyros and deli sandwiches. Their \\\"New York\\\" bagels didn't impress me so I'm not sure if I'll be back anytime soon to try other items on their menu.  Sad face.",
    },
    {"stars": 4, "text": "Great place, great service and friendly people"},
    {
        "stars": 1,
        "text": "After the UYE @ Herbs and Rye was over there was talk of tacos, the crew all ended up going to another destination, but since I'm lazy I figured I'd check out the place 10 feet from my parked car.\\n\\nThe place is nothing more than a tiny shack with a big light up screen on top of it, they have menus on both sides of the windows, one in english and one in spanish. \\n\\nThey don't have a ton of variety, but everything is hand made, the tortillas are hand made, and mine were made to order.\\n\\nThe place wasn't really busy, which concerned me a little, but I thought I'd give it a try.\\n\\nI ordered a Carne Asada Taco and a Taco Al Pastor. I was a little surprised when I got my order, all there was on my plate was 2 tortillas with some meat on them, no lettuce, no cheese, nothing.\\n\\nThey do have a small toppings bar next to the window that had 2 salsas and a guac sauce, limes, cabbage, and jalapenos, on it, but I'm not really a fan of any of them.\\n\\nI squeezed some lime on to my meaty tortillas and gave them a try.\\n\\nThe Taco Al Pastor was pretty solid, the pork was cooked and seasoned well, but it was nothing special.\\n\\nThe Carne Asada Taco was rather disappointing, the beef was chewy and barely seasoned.\\n\\nThe tortillas were fresh and tasted pretty good, but I have to admit for $1.75 each I was expecting more than meat and a tortilla.\\n\\nThe only things saving this place from a 1 star review are the fact that the ladies were friendly, the food came out quick, and the al pastor was decent.\\n\\nIt will do in a pinch, but there are 3 other taco places within a block, so I'd say check them out first.\\n\\nOh and there are no tables or chairs or anywhere to sit, I had to sit in my car and eat my tacos",
    },
    {
        "stars": 0,
        "text": "I agree with Insider Pages, the staff is super rude for either dine-in or to-go, I guess I am not pretty enough or the right color. Beware of cashier 19. \\nThe manager is controlled by the staff. In this economy with those prices and that attitude: NO THANK YOU! Never again. \\nTry DaVinci Pizza down the road, the owner takes pride in his pizza and the taste is almost as good for half the price.",
    },
    {
        "stars": 0,
        "text": "I have NEVER written a review on ANYTHING, but I absolutely had to for this restaurant. I cooked Chinese food for years and preparing this food in such a bland way is hard to do, so bravo guys. I've ate here a few times and it's either ok or just plain not good, and I mean not good to the point where I will literally just toss it out rather than eat it. So take my review for what it is. I know the business and one review is not gonna make or break a restaurant, but they have definitely lost my family, friends and I as customers.",
    },
    {
        "stars": 0,
        "text": "I love cafe rio but this location was very disappointing. The staff was very rude and the salad that I ordered comes with cheese but the guy only gave me a pinch and told me if I wanted more than that it would cost $1 more. The other locations give you cheese and don't argue with their customers over it. Then I asked for limes and they gave me lemons instead and when I told then, he rolled his eyes at me, like really. This location is very stingy with their ingredients and the staff have poor attitudes. I Will NEVER be back to this location EVER again and I have advised several others to go to a different location so they don't go through the same hassle I did. Lack of customer service is prevalent here.\\nFYI: If you hate your job that much that you treat your customers like shit, then quit your job. Management shouldn't allow this to happen, PERIOD!!!!!!!",
    },
    {
        "stars": 1,
        "text": "My husband and I went to the Cheesecake Factory for lunch. PROS- no wait, friendly waiter, large menu. CONS- atmosphere was very warehouse/industrial, food was overpriced. We will not be going back.",
    },
    {
        "stars": 3,
        "text": "Bartender was knowledgeable, friendly and knew how to make my favorite drink (a boulevardier) without having to look it up.  Upon ordering my second one, I made a suggestion as to how he could improve it (more compari) and he did as told and the second drink was even better.\\n\\nI ordered the pig ears for curiosity's sake.  The texture was slightly off-putting (the portion size was too big), but they were well seasoned and the salsa that came with it was very delicious.",
    },
    {
        "stars": 2,
        "text": "This place certainly isn't new and fancy like many of the other locations on the strip, but it is an okay place to get a good night's rest. There were a lot of children running around and things were a bit dingy and run down, but the price is pretty awesome. Do beware of the additional resort fees, which do get you a coupon book with some decent stuff like a free premium ride at the adventure dome and 2 midway games, plus some deals on drinking and gambling. Resort fee also covered free wifi. There is a gym which was much nicer than I expected, but very difficult to find. Many people asked seem to not know where it was hidden and there are no helpful signs. I would suggest it be kept open 24 hours a day since this is the city that never sleeps, but the hours started early and ended semi late. The pool didn't appear to be anything worth checking out unless you are super hot, especially if you have used any of the other pools on the strip. We did have a problem with an alarm clock next door going off in the middle of the night, but staff did get it taken care of eventually. I also had a problem with my safe, which may have been forgetting my own code, and was impressed when security arrived prior to the maintenance man to verify my identification. Do beware the food at the buffet is not really edible. Overall I would stay here again, but mostly if I was with children or had a strange love for the free circus acts.",
    },
    {
        "stars": 3,
        "text": "One of the best massages I have had. Ive gone to manu 5 star resorts yet I still think Seth's massage is just as good as many of them -- yet at a fraction of the cost.\\n\\nBeware however that this is not a 5 star spa experience! Its a small office with tiny massage rooms and VERY thin walls so you can hear people talking, which is annoying.  The thin walls are a big downside to this place. However, Seth seems to understands these limitations so is willing to give discounts and great deals for his massages which makes me ignore the thin walls\\n\\nIf you like deep tissue,  and are willing to deal with a non-chain small biz massage office, dont want to pay alot for a massage. Btw, Seth is a biz owner and a great masseuse so he books fast and it will take a day or two to call you back. Be patient though!  I highly recommend Seth for a great deep tissue massage!!",
    },
    {
        "stars": 0,
        "text": "HORRIBLE! Got a manicure and polish started chipping after just a few hours! The worker that did manicure seemed uninterested and annoyed to be there while rushing through manicure. Overall poor experience. Will never go back",
    },
]

eli5 = [  # https://huggingface.co/docs/transformers/tasks/masked_language_modeling #
    {
        "text": "I did some research as a layman. One forum user [claims it contains](_URL_1_) 300mg of Transfluthrin, but I can't seem to find any SC Johnson or Raid site that corroborates that. Transfluthrin is a pyrethroid, related to a pesticide produced by Chrysanthemums called pyrethrum. The EPA has [scant information on pyrethroids](_URL_0_), but the consensus seems to be that low doses are mostly harmless."
    },
    {
        "text": "While Freud was successful in bringing applied psychology into mainstream awareness and practice, equally we still have some throw-backs to his now-unsupported theories.\n\nOne of those is the intense focus on childhood experience and upbringing including as you said believing that because their parents did X they learnt Y.\n\nIn many respects from a practical point of view knowing the exact learning history of a harmful belief is irrelevant to learning a more helpful one. I would also argue that many people's claims of where their beliefs originated has more to do with their narration of themselves rather than accurate summary about their own cognition.\n\nHOWEVER a caveat - many people may find identifying a potential learning history such as 'my parents did X' may find this makes it easier to change said belief. Without such a rationale people may not even identify what their beliefs are explicitly or acknowledge them as a learnt function (rather than an accurate understanding).\n\nFor example Patient A might believe all people are untrustworthy and abusive, thusly struggling to maintain relationships. Questioning their upbringing and what their parents taught them is not typically a valid way to introduce change of this belief, but believing that comes from how they were raised may illustrate that the belief is changeable rather."
    },
    {
        "text": "Marine biologists and geologists often have opportunities to travel, depending on what kind of employment you can land. Also, while in college you should look into studying abroad."
    },
    {
        "text": 'It\'s related to the "beat" period/frequency - there\'s a wiki article here: _URL_0_ (and also something very relevant here: _URL_1_ )\n\nThis happens if you have two notes that are *slightly* different in frequency. The interferences broduces a volume oscillation with a frequency equal to the difference in frequencies. You can hear this if you\'re trying to tune a guitar. If you\'re off by like 5 Hz, you hear a rapid "wawawawawawawa" as the volume oscillates at 5 Hz. As you bring the string in tune, the beat frequency gets slower and slower ("wawawawaw waaa waaaa waaaaaaaaaa") as the difference in frequencies goes to zero.'
    },
    {
        "text": 'I would give you the exact details, but I actually found a nice little website that explains it all very simply. If you have further questions, I will be happy to answer; but I think the "What\'s Going On?" section answers your question nicely.\n\n_URL_0_'
    },
    {
        "text": "The diamagnetic material will have an induced field in the opposite direction of the exciting material, pushing the field lines somewhat out and away from the wall, depending on the magnetic susceptibility of the material. Superconductors have a magnetic susceptibility of -1 and are perfect diamagnets, so will completely expel the field lines. For a weaker diamagnet (everything else) the field lines will still penetrate the wall but will be attenuated and 'flattened' a bit."
    },
    {
        "text": "Ease of use usually picks the winner, and the resulting decline in usage picks the loser.\n\nIn your example, [*gaol*](_URL_0_) is still used in the UK and Australia, but not nearly as much as *jail*. *Gaol* uses more column width (which has given *jail* the nod in Australian newspapers) and it's also easily misread, usually as *goal*. If the trend continues, eventually everyone will spell it *jail*, and *gaol* will become an archaic spelling. So it is with language."
    },
    {
        "text": "So it's kind of outside the scope of the effect of diet on genetically small ethnic groups - e.g. \"pygmies\"; but the post WW II economic changes in Japan are a classic case of a people who were stereotypically small, but only due to general dietary/protein scarcity. In the japanese economic boom of the late 1950's and 1960s, protein became much more available to the population at large. This had some interesting economic effects: school classrooms and student desks were too small. The school infrastructure had been sized for the steretypical small japanese population; but with the increased availability of dietary proteins during critical childhood development years, they grew to sizes similar to people in other developed economies. I also have some friends who grew up in former communist states in Eastern Europe in the 50's and 60's. Both of them are very small ~ 5' 1\" - 5' 3\". However, emigrating to the US and having children here, their children are very much taller than they are."
    },
    {
        "text": "> f I was given a book in a language I don't understand and get no help understanding it, given unlimited time Could I one day translate it into English?\n\nCould you (or I) do it ? Who knows. It has certainly been done. The best example that comes to my mind is Linear B. The bulk of the work cracking it was done by Michael Ventris, a self taught Linguist. But credit should also be given to Michael Chadwick. (And for the sake of completeness Alice Kober's contribution has been recently regarded as underrecognized.)\n\n_URL_1_\n\nIt's a great story. I thoroughly recommend Michael Chadwick's book, The Decipherment of Linear B:\n\n_URL_0_"
    },
    {
        "text": "I suspect that a room temperature superconductor (if even possible) would contain vortices (pools of non-superconducting material). It wouldn't perfectly super-conduct in all regions and there would be some heat loss, overall entropy would be created. Also, most superconductors can only handle a certain amount of current and will not super-conduct past that point. There's more than just a factor of temperature when it comes to superconducting. You have critical fields, current, and pressure."
    },
    {
        "text": "I am not an expert in this field, but I am a scientist and I read the first paper and looked over the others. Here is my impression:\n\n* The first paper is written in a very unusual fashion. It may be a thesis. I would be very surprised if it has seen peer review.\n\n* The \"operators\" are the researchers themselves. This is not a suitable design to avoid bias and conflicts of interest.\n\n* The experiment was not systematically designed and included only a small dataset. The authors note this themselves, so it's not clear to me why they didn't do a better job.\n\n* The \"anomalies\" that are reported are laughably ridiculous. For example, they report that when the operators wanted the robot to spend longer on the table, the robot did indeed spend longer on the table. They report p=0.02 for this effect and consider this significant (the other papers have similarly unimpressive p-values). This is where the real problems lie. First of all, this is not a particularly low probability. If an equivalent experiment were run 50 times and the null result (no psychokinesis) were true, we would expect to see a result at least this improbable once. We have no clue how many similar experiments were run prior to this publication. With such a simple experimental set-up, it is easy to run a very large number of trials. So why are so few reported? Have some previous experiments been omitted? It is not like a drug trial where the experiment can not be simply repeated as many times as you like. Even for large complex experiments, there are issues surrounding publication bias (i.e., people not publishing results they don't like). Here, where experimental repeats are trivial, alarm bells are very much ringing.\n\nMoreover, p=0.02 would not be considered significant by any Bayesian. Typically p=0.05 is used as a cut-off for statistical significance, but let us not forget that that value is essentially arbitrary. It is a reasonable value for many purposes, but p < 0.05 is not the be all and end all. Your choice of p-value for significance should really be determined by:\n\n(a) Your goal. Is it better to admit false positives or to avoid false negatives? If, for instance, you were trialling a new drug that could replace a drug that you know already works well, you don't want to risk accepting a false positive, so you should choose a more conservative p-value for significance, e.g., p = 0.01.\n\n(b) The prior probability. In other words, what is the burden of proof on the hypothesis that you are testing? If you show me that a drug known to act on sleep promoting pathways increases sleep at night with a p=0.02 chance that the result is a fluke, I'm willing to accept that it is likely correct. If you show me that people who eat a handful of jelly beans immediately gain 65 IQ points relative to those who eat a handful of skittles with a p=0.02 chance that the result is a fluke, I'm very likely going to conclude that the result is a fluke and ask for a more stringent proof of the result.\n\nFinally, the results here are frequently from multiple comparisons, which requires a reassessment of statistical significance. By that, I mean many different analyses were performed on the data and then the most significant ones were held up as impressive. However, every time you perform a new analysis, you are increasing the probability of finding a significant result by chance. That is not addressed by the authors.\n\nIn sum, this is just really really bad science, I'm afraid."
    },
    {
        "text": "Eat, pray, and love...\n\nNo, just kidding.\n\n1. Practice good hygiene\n2. Monitor energy balance (calories in vs. calories out)\n3. Cultivate close relationships and personal interests\n\nModerate your vices, and don't get too caught up in trying to live forever; life is too short."
    },
]

books = [
    {
        "en": "Madame Raquin, feeling the catastrophe near at hand, watched them with piercing, fixed eyes.",
        "fr": "Mme Raquin, sentant que le dénouement était proche, les regardait avec des yeux fixes et aigus.",
    },
    {
        "en": "Therese and Laurent, all at once, burst into sobs.",
        "fr": "Et brusquement Thérèse et Laurent éclatèrent en sanglots.",
    },
    {
        "en": "A supreme crisis undid them, cast them into the arms of one another, as weak as children.",
        "fr": "Une crise suprême les brisa, les jeta dans les bras l'un de l'autre, faibles comme des enfants.",
    },
    {
        "en": "It seemed to them as if something tender and sweet had awakened in their breasts.",
        "fr": "Il leur sembla que quelque chose de doux et d'attendri s'éveillait dans leur poitrine.",
    },
    {
        "en": "They wept, without uttering a word, thinking of the vile life they had led, and would still lead, if they were cowardly enough to live.",
        "fr": "Ils pleurèrent, sans parler, songeante la vie de boue qu'ils avaient menée et qu'ils mèneraient encore, s'ils étaient assez lâches pour vivre.",
    },
    {
        "en": "Then, at the recollection of the past, they felt so fatigued and disgusted with themselves, that they experienced a huge desire for repose, for nothingness.",
        "fr": "Alors, au souvenir du passé, ils se sentirent tellement las et écoeurés d'eux-mêmes, qu'ils éprouvèrent un besoin immense de repos, de néant.",
    },
    {
        "en": "They exchanged a final look, a look of thankfulness, in presence of the knife and glass of poison.",
        "fr": "Ils échangèrent un dernier regard, un regard de remerciement, en face du couteau et du verre de poison.",
    },
    {
        "en": "Therese took the glass, half emptied it, and handed it to Laurent who drank off the remainder of the contents at one draught.",
        "fr": "Thérèse prit le verre, le vida à moitié et le tendit à Laurent qui l'acheva d'un trait.",
    },
    {
        "en": "The result was like lightning. The couple fell one atop of the other, struck down, finding consolation, at last, in death.",
        "fr": "Ce fut un éclair, Ils tombèrent l'un sur l'autre, foudroyés, trouvant enfin une consolation dans la mort.",
    },
    {
        "en": "The mouth of the young woman rested on the scar that the teeth of Camille had left on the neck of her husband.",
        "fr": "La bouche de la jeune femme alla heurter, sur le cou de son mari, la cicatrice qu'avaient laissée les dents de Camille.",
    },
    {
        "en": "The corpses lay all night, spread out contorted, on the dining-room floor, lit up by the yellow gleams from the lamp, which the shade cast upon them.",
        "fr": "Les cadavres restèrent toute la nuit sur le carreau de la salle et manger, tordus, vautrés, éclairés de lueurs jaunâtres par les clartés de la lampe que l'abat-jour jetait sur eux.",
    },
    {
        "en": "And for nearly twelve hours, in fact until the following day at about noon, Madame Raquin, rigid and mute, contemplated them at her feet, overwhelming them with her heavy gaze, and unable to sufficiently gorge her eyes with the hideous sight.",
        "fr": "Et, pendant près de douze heures, jusqu'au lendemain vers midi, Mme Raquin, roide et muette, les contempla à ses pieds, ne pouvant se rassasier les yeux, les écrasant de regards lourds.",
    },
]

niv = [
    {  # Gensis 1:1
        "en": "In the beginning God created the heavens and the earth.",
        "he": "בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ׃",
    },
    {  # Gensis 1:2
        "en": "Now the earth was formless and empty, darkness was over the surface of the deep, and the Spirit of God was hovering over the waters.",
        "he": "וְהָאָ֗רֶץ הָֽיְתָ֥ה תֹ֨הוּ֙ וָבֹ֔הוּ וְחֹ֖שֶׁךְ עַל־פְּנֵ֣י תְה֑וֹם וְר֣וּחַ אֱלֹהִ֔ים מְרַחֶ֖פֶת עַל־פְּנֵ֥י הַמָּֽיִם׃",
    },
    {  # Gensis 1:3
        "en": "And God said, “Let there be light,” and there was light.",
        "he": "וַיֹּ֥אמֶר אֱלֹהִ֖ים יְהִ֣י א֑וֹר וַֽיְהִי־אֽוֹר׃",
    },
    {  # Gensis 1:4
        "en": "God saw that the light was good, and he separated the light from the darkness.",
        "he": "וַיַּ֧רְא אֱלֹהִ֛ים אֶת־הָא֖וֹר כִּי־ט֑וֹב וַיַּבְדֵּ֣ל אֱלֹהִ֔ים בֵּ֥ין הָא֖וֹר וּבֵ֥ין הַחֹֽשֶׁךְ׃",
    },
    {  # Gensis 1:5
        "en": "God called the light “day,” and the darkness he called “night.” And there was evening, and there was morning—the first day.",
        "he": "וַיִּקְרָ֨א אֱלֹהִ֤ים ׀ לָאוֹר֙ י֔וֹם וְלַחֹ֖שֶׁךְ קָ֣רָא לָ֑יְלָה וַֽיְהִי־עֶ֥רֶב וַֽיְהִי־בֹ֖קֶר י֥וֹם אֶחָֽד׃",
    },
    {  # Gensis 1:6
        "en": "And God said, “Let there be a vault between the waters to separate water from water.”",
        "he": "וַיֹּ֣אמֶר אֱלֹהִ֔ים יְהִ֥י רָקִ֖יעַ בְּת֣וֹךְ הַמָּ֑יִם וִיהִ֣י מַבְדִּ֔יל בֵּ֥ין מַ֖יִם לָמָֽיִם׃",
    },
    {  # Gensis 1:7
        "en": "So God made the vault and separated the water under the vault from the water above it. And it was so.",
        "he": "וַיַּ֣עַשׂ אֱלֹהִים֮ אֶת־הָֽרָקִיעַ֒ וַיַּבְדֵּ֗ל בֵּ֤ין הַמַּ֨יִם֙ אֲשֶׁר֙ מִתַּ֣חַת לָֽרָקִ֔יעַ וּבֵ֣ין הַמַּ֔יִם אֲשֶׁ֖ר מֵעַ֣ל לָֽרָקִ֑יעַ וַֽיְהִי־כֵֽן׃",
    },
    {  # Gensis 1:8
        "en": "God called the vault “sky.” And there was evening, and there was morning—the second day.",
        "he": "וַיִּקְרָ֧א אֱלֹהִ֛ים לָֽרָקִ֖יעַ שָׁמָ֑יִם וַֽיְהִי־עֶ֥רֶב וַֽיְהִי־בֹ֖קֶר י֥וֹם שֵׁנִֽי׃",
    },
    {  # Gensis 1:9
        "en": "And God said, “Let the water under the sky be gathered to one place, and let dry ground appear.” And it was so.",
        "he": "וַיֹּ֣אמֶר אֱלֹהִ֗ים יִקָּו֨וּ הַמַּ֜יִם מִתַּ֤חַת הַשָּׁמַ֨יִם֙ אֶל־מָק֣וֹם אֶחָ֔ד וְתֵֽרָאֶ֖ה הַיַּבָּשָׁ֑ה וַֽיְהִי־כֵֽן׃",
    },
    {  # Gensis 1:10
        "en": "God called the dry ground “land,” and the gathered waters he called “seas.” And God saw that it was good.",
        "he": "וַיִּקְרָ֨א אֱלֹהִ֤ים ׀ לַיַּבָּשָׁה֙ אֶ֔רֶץ וּלְמִקְוֵ֥ה הַמַּ֖יִם קָרָ֣א יַמִּ֑ים וַיַּ֥רְא אֱלֹהִ֖ים כִּי־טֽוֹב׃",
    },
    {  # Gensis 1:11
        "en": "Then God said, “Let the land produce vegetation: seed-bearing plants and trees on the land that bear fruit with seed in it, according to their various kinds.” And it was so.",
        "he": "וַיֹּ֣אמֶר אֱלֹהִ֗ים תַּֽדְשֵׁ֤א הָאָ֨רֶץ֙ דֶּ֗שֶׁא עֵ֚שֶׂב מַזְרִ֣יעַ זֶ֔רַע עֵ֣ץ פְּרִ֞י עֹ֤שֶׂה פְּרִי֙ לְמִינ֔וֹ אֲשֶׁ֥ר זַרְעוֹ־ב֖וֹ עַל־הָאָ֑רֶץ וַֽיְהִי־כֵֽן׃",
    },
    {  # Gensis 1:12
        "en": "The land produced vegetation: plants bearing seed according to their kinds and trees bearing fruit with seed in it according to their kinds. And God saw that it was good.",
        "he": "וַתּוֹצֵ֨א הָאָ֜רֶץ דֶּ֠שֶׁא עֵ֣שֶׂב מַזְרִ֤יעַ זֶ֨רַע֙ לְמִינֵ֔הוּ וְעֵ֧ץ עֹֽשֶׂה־פְּרִ֛י אֲשֶׁ֥ר זַרְעוֹ־ב֖וֹ לְמִינֵ֑הוּ וַיַּ֥רְא אֱלֹהִ֖ים כִּי־טֽוֹב׃",
    },
]

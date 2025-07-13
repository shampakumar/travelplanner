
#!pip install tavily-python

import google.generativeai as genai
from tavily import TavilyClient
from google.colab import userdata

#Sample code to search internet.
st.title('Travel Planner')
tavily_client = TavilyClient("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") 
response = tavily_client.search(
    query="what is the date today"
)


data_load_state = st.text(response)

genai.configure(api_key="AIzaSyCIq7aePgTf98nlZGnnN21_QrHZINi4BCs")
modelChosen = 'gemini-2.0-flash'
model = genai.GenerativeModel(modelChosen)



#response = model.generate_content("What is the date today?")
#print(response)

"""# **Travel Planner**"""



class TravelPlanningAssistant:
  def __init__(self):
    self.destination = ""
    self.duration = ""
    self.budget = ""
    self.interests = [] #array not a str
    self.travel_style = ""

  def get_travel_info(self):
    print(f"Welcome to Travel buddy...")
    print("="*60)

    self.destination = input("Where do you want to go? ").strip()
    self.duration = input("How many days? ").strip()
    self.budget = input("What's your budget range? (500-1000, midrange, luxury)").strip()

    print(f"\nWhat are you interested in? (seperate with commas)")
    print("Examples : food, culture, adventure, nature, shopping, history")
    interests_input = input("Interest: ").strip()
    self.interests = [interest.strip() for interest in interests_input.split(',') if interest.strip()]

    print("\nTravel Style")
    print(f"1. Backpacker/Budget")
    print(f"2. Comfort/Mid-range")
    print(f"3. Luxury")
    print(f"4. Adventure")
    print(f"5. Cultural/Historical")
    style_choice = input("Choose (1-5): ").strip()

    styles= {
        "1":"Backpacker/Budget",
        "2":"Comfort/Mid-range",
        "3":"Luxury",
        "4":"Adventure",
        "5":"Cultural/Historical"
    }

    self.travel_style = styles.get(style_choice,"mid-range")

  def research_desitination(self):
    print(f"\n Researching Destination {self.destination}...")

    research_queries = [
        f"{self.destination} travel guide 2025-2026",
        f"{self.destination} best attractions things to do",
        f"{self.destination} travel safety current situation",
        f"{self.destination} weather climate best time to visit",
        f"{self.destination} budget costs accomodation and food",
    ]

    all_research = {}

    for query in research_queries:
      try:
        print(f"Searching : {query}....")
        results = tavily_client.search(query=query, max_results=3)
        research_text = ""
        for result in results.get('results',[]):
          research_text += f"Sources : {result.get('title','Unknown')}\n"
          research_text += f"{result.get('content','No Content')}\n\n"
        all_research[query] = research_text
      except Exception as e:
        print(f"Error Searching : {query}: {str(e)}")
        all_research[query] = "No information available"
    return all_research

  def create_travel_plan(self, research_data):
    print(f"Creating your personalizd travel plan....")

    combined_research = ""
    for query, content in research_data.items():
      combined_research += f"=== {query} ===\n{content}\n\n"

    prompt = f"""
    You are an expert travel planner. Create a comprehensive and detailed travel plan based on:

    DESTINATION : {self.destination}
    DURATION: {self.duration}
    BUDGET:{self.budget}
    INTERESTS:{self.interests}
    TRAVEL_STYLE:{self.travel_style}

    RESEARCH DATA: {combined_research[:8000]}

    Create a detailed plan with:

    1.**DESTINATION OVERVIEW**
      -Brief description and highlights
      -Best time time to visit
      -Cultural tips and etiquette

    2.**SAFETY & PRACTICAL INFO**
      -Current safety situation
      -Visa Requirements
      -Currency exchange and payment method
      - Language Tips

    3. **DAILY ITENARY**
      -Day-by-day plan for {self.destination}
      -Mix of must-see attractions and personal interests
      -Include travel time between locations

    4.**FOOD AVAILABE**
      -Country specific cusisine information
      -Veg food vs Non-veg food based information for veg or vegal travellers

    5. **EMERGENCY CONTACT**
      -Imporatant phone numbers
      -Embassy/consulate info

    Make it practical, detailed, and personalized to their interests and budget
    """

    try:
      response = model.generate_content(prompt)
      return response.text
    except Exception as e:
      print(f"Error creating travel plan : {str(e)}")

  def get_current_alerts(self):
    print(f"Checking current travel alerts... Travel advisory")
    try:
      alert_query = f"{self.destination} travel advisory warning alert 2025 2026"
      result = tavily_client.search(query=alert_query, max_results=3)

      alerts = ""
      for result in results.get('results',[]):
        alerts += f"⚠️ {result.get('title','Unknown')}\n"
        alerts += f"⚠️ {result.get('content','No Content')[:200]}\n\n"
      return alerts if alerts else "No current travel alerts found!!"
    except Exception as e:
      return f"Eroor checking alerts: {e}"

  def run(self):
    try:
      self.get_travel_info()
      research_data = self.research_desitination()
      alerts = self.get_current_alerts()

      travel_plan = self.create_travel_plan(research_data)

      print("\n" + "="*60)
      print(f"Your personalized travel plan is.....")
      print("="*60)
      print(travel_plan)

      print("\n" + "="*60)
      print(f"Current travel alerts.....")
      print("="*60)
      print(alerts)

      print("\n" + "="*60)
      print(f"Travel Summary ")
      print(f"Destination : {self.destination}")
      print(f"Duration : {self.duration}")
      print(f"Budget : {self.budget}")
      print(f"Interests : {self.interests}")
      print(f"Style : {self.travel_style}")

      save = input("\n Save this plan to file? (y/n): ").strip().lower()
      if save == 'y':
            filename = f"{travel_plan_my_file}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Travel plan")
                f.write(travel_plan)
                f.write(alerts)
            print(f"Plan saved")
    except Exception as e:
            pass

def main():
  assistant = TravelPlanningAssistant()

  while True:
    try:
      assistant.run()

      another = input("\n Plan another trip (y/n) : ").strip().lower()
      if another != 'y':
        print(f"Happy travels!")
        break
      assistant = TravelPlanningAssistant()
    except Exception as e:
      print(f"Goodbye")
      break

# if __name__ == "__main__":
#   main()

"""# New section"""
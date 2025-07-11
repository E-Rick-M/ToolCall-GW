from openai import OpenAI

client=OpenAI(base_url="http://localhost:11434/v1",api_key="ollama")

def get_temperature(city:str)-> float:
    """
    get the current temperature of the given city
    """
    return 20.0

def send_to_openAI(history:list, prompt:str)-> str:
    history.append({"role":"user", "content":prompt})
    response = client.chat.completions.create(
    model="qwen3:4b",
    messages=history
    
    )
    reply = response.choices[0].message.content
    return reply
        
def main():
    history=[]
    user_input=input("Your Message: ")
    
    history.append({"role":"user", "content":user_input})
    
    prompt=f"""
        You are a helpfull assistant. Answer the user's Question in a friendly way.
        
        You can also use tools if you feel like they help you provide a better answer
        -get_temperature(city:str)-> float : Get the temperature for a given City.
        
        If you want to use one of these tools, you should output the tool name and its arguments in the following format.
        tool_name:arg1, arg2, ...
        
        For example:
        get_temperature:Mombasa
        
        with that in mind answer the users Question:
        <question>
        {user_input}
        </user_question>
        
        If you Request a Tool, Please Output only the tool call (as described above) and nothing else.
        """
    reply=send_to_openAI(history,prompt)
    
    history.append({"role": "assistant", "content": reply})
    print('---------------')
    print(reply.endswith("get_temperature:"))
    print('---------------')
    
    if reply.strip().startswith("get_temperature:") or "get_temperature:" in reply:
        
        # lines = reply.strip().splitlines()
        # tool_call_line = next((line for line in lines if line.strip().startswith("get_temperature:")), None)

        # if tool_call_line:
        # arg = tool_call_line.split(":",1)[1].strip()


        arg=reply.split(":",1)[1].strip()
        
        temperature=get_temperature(arg)
        adjusted_prompt=f""" 
        You are a Helpful assistant. Answer the users Question in a friendly way.
        
        Here's the user's Question
        <question>
        {user_input}
        </user_question
        
        You requested to use the get_temperature tool for the city "{arg}"
        Here's the Result of excecuting that tool:
        The current Temperature in {arg} is {temperature}ºC.
        """
        # print(adjusted_prompt)
        # response = client.chat.completions.create(
        # model="qwen3:4b",
        # messages=[
        # {"role": "system", "content": "You are a helpful assistant."},
        # {"role": "user", "content": adjusted_prompt}
        # ]
    
        # )
        # reply = response.choices[0].message.content
        # print('---------------')
        # print(reply)
        weather_update=send_to_openAI(history,adjusted_prompt)
        print(f"Assistant : {weather_update}")
       
    else:
        print(reply) 

if __name__ == "__main__":
    main()

from openai import OpenAI
import json

client=OpenAI(base_url="http://localhost:11434/v1",api_key="ollama")



tools=[
    {
        "type":"function",
        "name":"get_temperature",
        "description":"Get current temperature of a given location",
        "parameters":{
            "type":"object",
            "properties":{
                "city":{
                    "type":"string",
                    "description":"City to get the temperature"
                }
            },
            "additionalProperties": False,
            "required":["city"]
        }
        
    }
]

def get_temperature(city:str)-> float:
    """
    get the current temperature of the given city
    """
    return 20.0


available_functions={
    "get_temperature":get_temperature
}


def excecute_tool_call(tool_call)->str:
    fn_name = tool_call.function.name
    fn_args = json.loads(tool_call.function.arguments)

    
    if fn_name in available_functions:
        function_tool_call=available_functions[fn_name]
        try:
            return function_tool_call(**fn_args)
        except Exception as e:
            return f"Error calling {fn_name}: {e}"
    return f"Unknown tool: {fn_name}"



def send_to_openAI(history:list):
    # history.append({"role":"user", "content":prompt})
    
    response = client.chat.completions.create(
    model="qwen3:4b",
    messages=history,
    tools=tools
    
    )
    message = response.choices[0].message
    print(response)
    print('----------------')
    print(message)
    print('----------------')
    
    # history.append({"role":"assistant", "content":message})
    
    if message.tool_calls:
        for tool_call in message.tool_calls:
            print(f"Tool call requested: {tool_call.function.name}")
            result=excecute_tool_call(tool_call)

            history.append({
                "role": "tool",
                "name": tool_call.function.name,
                "content": str(result)
            })
             
            follow_up = client.chat.completions.create(
            model="qwen3:4b",
            messages=history
        )
        reply = follow_up.choices[0].message.content
        print(f"Assistant: {reply}")
        history.append({"role": "assistant", "content": reply})
        return reply

    elif message.content:
        reply = message.content
        print(f"Assistant: {reply}")
        history.append({"role": "assistant", "content": reply})
        return reply
        
def main():
    history=[]
    while True:
        
        user_input=input("Your Message (type 'Exit' to end the conversation): ").lower()
        
        if user_input=="exit":
            break
        
        history.append({"role":"user", "content":user_input})
        
        system_message = {
            "role": "system",
            "content": """
            You are a helpful assistant.

            You can use tools to help answer user questions.

            Available tool:
            - get_temperature(city: str): Gets the current temperature for a given city.
            """
        }

        history.append(system_message)
        
        # prompt=f"""
        #     You are a helpfull assistant. Answer the user's Question in a friendly way.
            
        #     You can also use tools if you feel like they help you provide a better answer
        #     -get_temperature(city:str)-> float : Get the temperature for a given City.
            
        #     If you want to use one of these tools, you should output the tool name and its arguments in the following format.
        #     tool_name:arg1, arg2, ...
            
        #     For example:
        #     get_temperature:Mombasa
            
        #     with that in mind answer the users Question:
        #     <question>
        #     {user_input}
        #     </user_question>
            
        #     If you Request a Tool, Please Output only the tool call (as described above) and nothing else.
        #     """
        reply=send_to_openAI(history)
        
        print(f"Overall Assistant Reply Message: {reply}")
        
        # history.append({"role": "assistant", "content": reply})
        # print('---------------')
        # print(reply.endswith("get_temperature:"))
        # print('---------------')
        
        # if reply.strip().startswith("get_temperature:") or "get_temperature:" in reply:

        #     arg=reply.split(":",1)[1].strip()
            
        #     temperature=get_temperature(arg)
        #     adjusted_prompt=f""" 
        #     You are a Helpful assistant. Answer the users Question in a friendly way.
            
        #     Here's the user's Question
        #     <question>
        #     {user_input}
        #     </user_question
            
        #     You requested to use the get_temperature tool for the city "{arg}"
        #     Here's the Result of excecuting that tool:
        #     The current Temperature in {arg} is {temperature}ºC.
        #     """
        #     weather_update=send_to_openAI(history,adjusted_prompt)
        #     print(f"Assistant : {weather_update}")
        
        # else:
        #     print(reply) 

if __name__ == "__main__":
    main()

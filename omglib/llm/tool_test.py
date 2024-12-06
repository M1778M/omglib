import tools
import asyncio


if __name__ == "__main__":
    assert tools.run_py("print('This is working just right')") == {'run_status':'Successful',"error_message":"<No Error>"}
    assert tools.run_py("gimmesomeerror_SADS!()*()")['run_status'] == "Failed"
    assert list(tools.get_weather("New York")) == ['location', 'temperature', 'unit']
    
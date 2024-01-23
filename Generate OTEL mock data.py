import os
import json
from faker import Faker

fake = Faker()

def generate_mock_event(start_time, end_time):
    return {
        "traceId": fake.uuid4(),
        "spanId": fake.uuid4(),
        "parentSpanId": fake.uuid4(),
        "INFA_OP_TYPE": fake.random_element(elements=('DELETE_EVENT', 'INSERT_EVENT','UPDATE_EVENT')),
        "name": fake.random_element(elements=('operationA', 'operationB')),
        "startTimeUnixNano": start_time,
        "endTimeUnixNano": end_time,
        "droppedAttributesCount": 1,
        "events": [
            {
                "timeUnixNano": str(int(end_time) + 123),
                "name": "event-with-attr",
                "attributes": [
                    {
                        "key": "span-event-attr",
                        "value": {"stringValue": "span-event-attr-val"}
                    }
                ],
                "droppedAttributesCount": 2
            },
            {
                "timeUnixNano": str(int(end_time) + 123),
                "name": "event",
                "droppedAttributesCount": 2
            }
        ],
        "droppedEventsCount": 1,
        "status": {
            "message": "status-cancelled",
            "code": 2
        }
    }

def generate_mock_data():    
    start_time = str(int(fake.date_time_this_decade().timestamp() * 1e9))
    end_time = str(int(start_time) + fake.random_int(min=1000000, max=100000000))  # Randomizes duration between 1ms and 100ms

    return {
        "resourceSpans": [
            {
                "resource": {
                    "attributes": [
                        {
                            "key": "resource-attr",
                            "value": {"stringValue": "resource-attr-val-1"}
                        },
                        {
                            "key": "prac_id",
                            "value": {"stringValue": fake.random_element(elements=('A', 'B', 'C','D','E','F','G','H','I','J'))}
                        },
                    ]
                },
                "scopeSpans": [
                    {
                        "scope": {},
                        "spans": [
                            generate_mock_event(start_time, end_time)
                        ]
                    }
                ]
            }
        ]
    }

if __name__ == "__main__":
    num_events = 10  # Adjust the number of events as needed
    mock_data = [generate_mock_data() for _ in range(num_events)]

    with open(os.path.dirname(os.path.realpath(__file__)) + "/mock_data.json", "w") as f:
        json.dump(mock_data, f, indent=2)

    print(f"Mock data generated and saved to 'mock_data.json'")
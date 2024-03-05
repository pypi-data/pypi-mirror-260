
  

# CELERABIT PIPELINE INTEGRATION TOOLS

  

This package helps to integrate CI/CD processes with [celerabit platform](https://www.celerabit.com)

  

**REQUIEREMENTS**

  

None.

**USAGE**

  

```

python -m celerabitpipelineintegration <operation> [ags] [<flags>]

```

  

## Operation `authenticate`

Generates an [authentication token](https://app.celerabit.com). This token will be input for secure operations.

  

### **Examples**

  

- Generate authentication token

  

```sh

python -m celerabitpipelineintegration authenticate login "myemail@mydomain.com" password "secretpassword"

```

You must replace `myemail@mydomain.com` and `secretpassword` for your valid credentials in celerabit platform.

The Output of this operation is an alphanumeric token like this:

```

eyJhbGciOiJIUzI1NiIsInR5cCI6Ikicm9sZXMiOm51bGx9LCJpYXQiOjE2NzIyNTQyMDAsImV4cCI6MTY3MjI2MTQwMH0cWBm8Iua2sUFkHbr89epcfN9EtwBDKtqoLMUtdXJSk

```

  

## Operation `run`

This operation runs a performance testing scenario and wait for it to finish.  

> CELERABIT PIPELINE INTEGRATION TOOLS only runs scenarios API and UX type scenarios.

  

### **Examples**

  

- Runs a scenario and waits for the execution to finish. If the scenario has not finished in 120 seconds (2 minutes), it will throw an exception.

  

```sh

python -m celerabitpipelineintegration run token "nR5cCI6Ikicm9sZXMiOm51bGYXQiOjE2NzIyNDAsImV4cCI6MTY3MjI2MTQwMH0" client "My client Name" application "My application Name" scenario "My scenario code" timeout 120

```

You must replace `nR5cCI6Ikicm9sZXMiOm51bGx9LCJpYXQiOjE2NzIyNTQyMDAsImV4cCI6MTY3MjI2MTQwMH0` for a valid authentication token, `My client Name` for your client name in celerabit platform, `My application Name` for the name of the application in celerabit platform aich the scneario belongs to, and `My scenario code` for the code of the existing scenario that you want to run.

>If **verbose mode** is needed to show detailed execution information, you can add the flag `-v` at the end of the execution command line.

  

>Note that previous command specifies a **timeout** this means: if scenario execution takes more than 120 seconds (`timeout 120`), command `python -m celerabitpipelineintegration run` will fail.

#### **Json output when API scenario is run**  

When you run an API scenario, the output of the command is a json object that specifies the new job id:

```

{
"jobId": 1158298,
"status": "SUCCESS",
"dateCreated": "2023-01-01T17:01:01.851Z",
"duration": 178.913196,
"kpiLatency": 3000,
"kpiErrors": 5,
"kpiThroughput": 100,
"kpiDeviation": 3000,
"metricLatency": 27.74,
"metricErrors": 0.35,
"metricThroughput": 1659057.06,
"metricDeviation": 52.36,
"complianceLatency": 199.08,
"complianceErrors": 192.94,
"complianceThroughput": 200,
"complianceDeviation": 198.25
}

```

Ih this response:
  

| Attribute | Type | Description |
| -- | -- | -- |
| `jobId` | Job Info | Id corresponding the new created job for this scenario run. |
| `status` | Job Info | Indicates if the job finished in `SUCCESS` or `ERROR` status. |
| `dateCreated` | Job Info | Date and time the job starts its execution. |
| `duration` | Job Info | Indicates the seconds the job took to finalize. |
| `kpiLatency` | KPI | Objective value defined for the scenario average latency. |
| `kpiErrors` | KPI | Objective value defined for the scenario errors percentage. |
| `kpiThroughput` | KPI | Objective value defined for the scenario capacity (requests attended per minute). |
| `kpiDeviation` | KPI | Objective value defined for the standard deviation for scenario average latency. |
| `metricLatency` | Metric | Measured value for the scenario average latency in this run (For this `jobId`). |
| `metricErrors` | Metric | Measured value for the scenario errors percentage in this run (For this `jobId`). |
| `metricThroughput` | Metric | Measured value for the capacity (requests attended per minute) in this run (For this `jobId`). |
| `metricDeviation` | Metric | Measured value for the standard deviation for scenario average latency in this run (For this `jobId`). |
| `complianceLatency` | Compliance | Latency compliance (latency metric vs latency KPI). |
| `complianceErrors` | Compliance | Errors percentage compliance (Errors percentage metric vs Errors percentage KPI). |
| `complianceThroughput` | Compliance | Capacity compliance (Capacity metric vs Capacity KPI). |
| `complianceDeviation` | Compliance | Deviation compliance (Deviation metric vs Deviation KPI). |

  #### **Json output when UX scenario is run**  

When you run an UX scenario, the output of the command is a json object that specifies the new job id:

```
{
    "target": "MyApplication",
    "scenarioId": 1234567,
    "scenario": "Transference in valley time",
    "jobId": 7654321,
    "status": "FINISHED",
    "dateCreated": "2024-02-13T19:53:34.205Z",
    "duration": 17.544,
    "uxResults": {
        "date": "13-Feb-2024 15:06:38",
        "performance": {
            "value": 22,
            "color": "BAD"
        },
        "timeToFirstContent": {
            "value": "4.9 s",
            "color": "BAD"
        },
        "timeToInteractive": {
            "value": "13.7 s",
            "color": "BAD"
        },
        "timeToBiggestContent": {
            "value": "8.3 s",
            "color": "BAD"
        },
        "blockingTime": {
            "value": "2,580 ms",
            "color": "BAD"
        },
        "biggestFiles": [
            {
                "url": "https://d.files.com/6317a229ebf7723658463b4b/652de89b06c9ce7d25ef6%20con%us.png",
                "size": "1,028.19 KB",
                "color": "BAD"
            },
            {
                "url": "https://d.files.com/web_widget/classic/latest/web-widget-main-e46caa3.js",
                "size": "908.93 KB",
                "color": "BAD"
            },
            {
                "url": "https://d.files.com/6317a229ebf7723658463b4b/js/efre.f3214c347.js",
                "size": "749.69 KB",
                "color": "BAD"
            },
            {
                "url": "https://d.files.com/6317a229ebf7723658463b4b/css/uhu89ui.145588cb2.min.css",
                "size": "722.48 KB",
                "color": "BAD"
            },
            {
                "url": "https://www.gstatic.com/recaptcha/releases/x5WWoE57Fv0d6ATKsLDIAKnt/recaptcha__en.js",
                "size": "489.62 KB",
                "color": "MEDIUM"
            },
            {
                "url": "https://www.googletagmanager.com/gtm.js?id=GTM-PS6JT5F",
                "size": "334.81 KB",
                "color": "MEDIUM"
            },
            {
                "url": "https://www.googletagmanager.com/gtag/js?id=G-SEM5N1VSYQ&l=dataLayer&cx=c",
                "size": "284.14 KB",
                "color": "MEDIUM"
            },
            {
                "url": "https://d.files.com/6317a229ebf7723658463b4b/65a03c52be6df16c2r%20taa%201.svg",
                "size": "279.45 KB",
                "color": "MEDIUM"
            },
            {
                "url": "https://www.googletagmanager.com/gtag/js?id=G-3ZK85EP37Q&cx=c&_slc=1",
                "size": "251.18 KB",
                "color": "MEDIUM"
            },
            {
                "url": "https://connect.facebook.net/en_US/werihu9ufijn.js",
                "size": "214.37 KB",
                "color": "MEDIUM"
            }
        ],
        "stepsTime": {
            "pre": "800 mls",
            "post": "0 mls"
        }
    }
}
```


## Operation `eval-job-results`

Receives the json structure resulting from executing a scenario and evaluates its compliance by giving a tolerance level.

  

### **Examples**

  

- Receive the json structure resulting of executing an scenario and evaluates its compliance giving a tolerance level.

  

```sh
TOLERANCE="latency=0.8,throughput=0.5,errors=0.95,deviation=0.2"

python -m celerabitpipelineintegration eval-job-results job-result "${EXEC_RESULT}" tolerance "${TOLERANCE}
```

>The output of this command is an string with the compliance validation errors. If there is not, the string will be empty.

  

In this example, the `EXEC_RESULT` variable contains the **json** structure returned by using the [run](#Operation-run) operation. The values sent in the `TOLERANCE` parameter specify the minimum percentage of compliance accepted for the executed scenario. 

#### **Tolerance for API scenarios**

The tolerance string for API scenarios is as shown in the example above. 

```sh
# The values in the tolerance string are case-sensitive
TOLERANCE="latency=0.8,throughput=0.5,errors=0.95,deviation=0.2"
```

The following table explains their values:

| Performance dimension | Tolerance (Minimun compliance) |
| -- | -- |
| `latency` | `0.8` (80%) |
| `throughput` | `0.5` (50%) |
| `errors` | `0.95` (95%) |
| `deviation` | `0.2` (20%) |

#### **Tolerance for UX scenarios**

Tolerance string for UX scenarios specifies the minimun range of tolerance expected for the consolidated metric **Performance**.

The valid values for performance are:
| Value | Performance range |
| -- | -- |
| GOOD | Performance grather than 0.9 |
| MEDIUM | Performance Between 0.5 and 0.89 |
| BAD | Performance Between 0 and 0.49 |

Performance string has the following example structure:

```sh
# The values in the tolerance string are case-sensitive
TOLERANCE="performance=MEDIUM"
```
The following table explains their values:

| Performance dimension | Tolerance (Minimun compliance) | Comments |
| -- | -- | -- |
| `performance` | MEDIUM | This indicates that performance indicator must be in the reage MEDIUM |


#### **Default tolerance**
If no **Tolerance** value is specified the default values will be:

##### API scenario
The default tolerance tolerance string for API scenarios is:
```sh
"latency=0.8,throughput=0.5,errors=0.95,deviation=0.3"
```

##### UX scenario
The default tolerance tolerance string for UX scenarios is:
```sh
"performamce=MEDIUM"
```

  

## Operation `last-status`

This operation returns the details of the last job execution for a given scenario.

  

### **Examples**

  

```sh

python  -m  celerabitpipelineintegration  last-status  token  "nR5cCI6Ikicm9sZXMiOm51bGYXQiOjE2NzIyNDAsImV4cCI6MTY3MjI2MTQwMH0"  client  "My client Name"  application  "My application Name"  scenario  "My scenario code"

```

  

You must replace `nR5cCI6Ikicm9sZXMiOm51bGx9LCJpYXQiOjE2NzIyNTQyMDAsImV4cCI6MTY3MjI2MTQwMH0` for a valid authentication token, `My client Name` for your client name in celerabit platform, `My application Name` for the name of the application in celerabit platform aich the scneario belongs to, and `My scenario code` for the code of the existing scenario that you want to run.

  

The output of this operation is same as [`run` operation](#Operation-run).
# Approach Disclaimer

In this assignment, i have decided on a Right to Left approach. 
Usually when we design an architecture solution for a data platform, we we'll want to understand the data sources, design the different components, understand the current state and the business requirements, select the tech stack, design the ETL layers for the DWH/Lake-house, In this approach we know what are the desired specific use cases we need to answer (2 dashboards), and we'll build our architecture and data platform design from the target (right) to the source (left).

### Known facts & assumptions:
- the company is using AWS stack, but would prefers **cloud agnostic solution**. => the suggested will lean as much as possible to an agnostic solution, but as mentioned that AWS is being used today, we'll suggest a solution based on aws components, but still to be headless & agnostic architecture as possible.
- Largest client owns **25%** of the records in the database => at this stage i will assume that this fact will reflect the entire database including the given entity.
- document size is usually less then 2KB but can **sometime** be up to **2MB** => 
  - i will assume this will be a ratio of 10% = 2MB / 90% = 2KB.
  - i will assume that **document** relate also to the given entity document.
- There are currently **1B** documents in the **database** => this relate to the entire **database** , so i will assume that the majority of the documents are derived from the relevant **main entity** collection, and that it size is a major subset of the total 1B records, so i will calculate that in the **main entity** collection there are at least 800M documents, the rest of the 200M are for other entities collections, a ratio of 80% / 20%.  
- the client analysis dashboard is with a latency of seconds.
- the senior leadership dashboard is reviewed weekly.
- there are **hundreds of requests per day** by supported by different support team at different locations for a **typical clients**.  => 
  - each client create hundreds of requests per day.
  - **25%** of the records are from one client.
- current solution will sustain more then 10X increase in database size.
### sizes estimations

**general**
database size **(current state)**:
 ```
(90% of 1B: small documents) {900,000,000 X 2KB} = 1.657 TB 
+
(10% of 1B: small documents) {100,000,000 X 2MB} = 190.75 TB
```

database size **(expected state that should be supported)**:
```
192 TB X 10 = 1920 TB = 2 PB
```
**the big client**:
```
(25% of the records) 25% of 2PB = **0.5PB**
```

**main entity** collection:
database size **(current state)**:
``` 
80% X 1.657 TB = 1.3 TB 
+
80% X 190.75 TB = 152 TB
```
database size **(expected state that should be supported)**:
```
80% X 2 PB = 1.6 PB
```
**the big client**:
```
80% X 0.5 PB = 0.4 PB
```

**amounts of documents**
**current state** 1B in total
we don't know for how long is this history relates to, 1 / 2 / 3 ..n years of data.
**i will assume** this is for 1 year.
hundreds of documents per client per day.
we don't know how many clients.

### points to **consider**
the size of data will grow to about 2 PB in total (need to be able to handle big data).
dashboard should be updated with latency of seconds.
we are looking for an agnostic cloud solution.

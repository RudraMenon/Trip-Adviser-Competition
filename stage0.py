
import sys
jobs, workers = generate_jobs()

jobClasses = []
workerClasses = []

class Job:
  def __init__(self, name, can_begin, tasks, task_time, priority):
    self.name = name
    self.can_begin = can_begin
    self.tasks = tasks
    self.task_time = task_time
    self.priority = priority
    self.tasksDone = 0
    self.startTime = -1
    self.complete = False

  def setStartTime(self,time):
      if self.startTime == -1:
          self.startTime = time

class Worker():
    def __init__(self, name, doneWorking):
        self.name = name
        self.doneWorking = 0
        self.job = None

    def isFree(self, time):
        if self.doneWorking <= time:
            return True
        return False

def makeJobClasses():
    global jobClases

    for job in jobs:
        job = job.__repr__().split(" ")
        name = job[1]
        tasks = int(job[2])
        task_time = int(job[3])
        can_begin = int(job[4])
        priority = int(job[5])
        newJob = Job(name,can_begin,tasks,task_time,priority)
        jobClasses.append(newJob)

def makeWorkerClasses():
    global workerClasses

    for worker in workers:
        newWorker = Worker(worker, 0)
        workerClasses.append(newWorker)

def calcCost(job, time):
    job.setStartTime(time)
    timeToComplete = (job.tasks-job.tasksDone)*job.task_time
    endTime = timeToComplete + job.startTime
    cost = job.priority*(((endTime-job.can_begin)**2 + (endTime-job.startTime)**2)**0.5)
    return cost

def getLowCostJob(time):
    lowestCost = calcCost(jobClasses[0], time)
    bestJob = jobClasses[0]
    for job in jobClasses:
        if calcCost(job, time) < lowestCost:
            bestJob = job
    return bestJob

def getFreeWorker(time):
    for worker in workerClasses:
        if worker.isFree(time):
            return worker

    return False

makeJobClasses()
makeWorkerClasses()
time = 0

while len(jobClasses) >0 :
    bestJob = getLowCostJob(time)
    worker = getFreeWorker(time)
    if worker:
        worker.doneWorking = time + bestJob.task_time
        if worker.job != bestJob:
            sys.stdout.write(str(time)+ " " + worker.name + " " + bestJob.name + "\n")
        worker.job = bestJob
        bestJob.tasksDone +=1
        if bestJob.tasksDone >= bestJob.tasks:
            jobClasses.remove((bestJob))
    if not getFreeWorker(time):
        time += 1





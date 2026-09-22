
class plotting_regions:
  def __init__(self):
      self.figsize=(8,8)
      self.xlocs  = list(range(-180,181,15))
      self.ylocs  = list(range(-90, 91, 10))
      self.extent = [-180, 180, -90, 90]
      self.central_longitude = -80.0
      self.true_scale_latitude = 60.0
      self.mpro = 'nps'

class globe(plotting_regions):
  def __init__(self):
      self.figsize=(8,4)
      self.xlocs  = list(range(-180,181,30))
      self.ylocs  = list(range(-90, 91, 15))
      self.extent = [-180, 181, -90, 91]
      self.central_longitude  =  0.
      self.true_scale_latitude = 0.0
      self.mpro = 'platecarree'

class nh(plotting_regions):
  def __init__(self):
      self.figsize=(6,8)
      self.xlocs  = list(range(-180,181,15))
      self.ylocs  = list(range(0, 90, 10))
      self.extent = [-180, 180, 35, 90]
      self.central_longitude = -80.
      self.true_scale_latitude = 65.0
      self.mpro = 'nps'

class sh(plotting_regions):
  def __init__(self):
      self.figsize=(8,8)
      self.xlocs  = list(range(-180,181,15))
      self.ylocs  = list(range(-90, 0, 5))
      self.extent = [-180, 180, -80, -50]
      self.central_longitude = -80.
      self.true_scale_latitude = -65.0
      self.mpro = 'sps'

class alaska(plotting_regions):
  def __init__(self):
      self.figsize=(8,8)
      self.xlocs  = list(range(-200, 0,10))
      self.ylocs  = list(range(55, 80, 5))
      self.extent = [-180, -120, 55, 80]
      self.central_longitude = -170.
      self.true_scale_latitude = 65.0
      self.mpro = 'nps'

class nbering(plotting_regions):
  def __init__(self):
      self.figsize=(8,6)
      self.xlocs  = list(range(-180,181,10))
      self.ylocs  = list(range(60,85, 5))
      self.extent = [-180, -120, 65, 75]
      self.central_longitude = -150
      self.true_scale_latitude = 70.0
      self.mpro = 'nps'

class sbering(plotting_regions):
  def __init__(self):
      self.figsize=(8,6)
      self.xlocs  = list(range(-180,181,10))
      self.ylocs  = list(range(50, 80, 5))
      self.extent = [-190, -155, 55, 65]
      self.central_longitude = -170.
      self.true_scale_latitude = 60.0
      self.mpro = 'nps'

class nsr(plotting_regions):
  def __init__(self):
      self.figsize=(8,4)
      self.xlocs  = list(range(-180,181,15))
      self.ylocs  = list(range(45, 91, 5))
      self.extent = [60, 195, 65, 83]
      self.central_longitude = 127.5
      self.true_scale_latitude = 70.0
      self.mpro = 'nps'

class ross(plotting_regions):
  def __init__(self):
      self.figsize=(8,4)
      self.xlocs  = list(range(-180,181,15))
      self.ylocs  = list(range(-80,-45, 5))
      self.extent = [150, 210, -80, -55]
      self.central_longitude = 180.
      self.true_scale_latitude = -65.0
      self.mpro = 'sps'


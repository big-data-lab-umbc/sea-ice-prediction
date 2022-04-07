#This function is used to combine ERA5 and ERA5T data

class combine:
		def combine_era(self,variables,missing_val):
				import numpy as np
		#Input: variables in ERA5/ERA5T [time,expver,latitude, longitude]
		#		missing_val: missing_values in the file
		#Output: new_variables [time, latitude, longitude]
				time_dim,expver_dim,lat_dim,lon_dim = variables.shape
				new_variables=np.empty([time_dim,lat_dim,lon_dim])
				for i in range(0,time_dim):
						for xx in range(0,lat_dim):
								for yy in range(0,lon_dim):
										if variables[i,0,xx,yy] != missing_val:
												new_variables[i,xx,yy] = variables[i,0,xx,yy]
										elif variables[i,1,xx,yy] != missing_val:
												new_variables[i,xx,yy] = variables[i,1,xx,yy]
										else:
												new_variables[i,xx,yy] = missing_val
				return new_variables


		def combine_era4d(self,variables,missing_val):
				import numpy as np
		#Input: variables in ERA5/ERA5T [time,expver,level,latitude,longitude]
		#		missing_val: missing_values in the file
		#Output: new_variables [time, level,latitude, longitude]
				time_dim,expver_dim,level_dim,lat_dim,lon_dim = variables.shape
				new_variables=np.empty([time_dim,level_dim,lat_dim,lon_dim])
				
				for i in range(0,time_dim):
						for j in range(0,level_dim):
								for xx in range(0,lat_dim):
										for yy in range(0,lon_dim):
												if variables[i,0,j,xx,yy] != missing_val:
														new_variables[i,j,xx,yy] = variables[i,0,j,xx,yy]
												elif variables[i,1,j,xx,yy] != missing_val:
														new_variables[i,j,xx,yy] = variables[i,1,j,xx,yy]
												else:
														new_variables[i,j,xx,yy] = missing_val
				return new_variables

				
				

/**********************************************
 * Self-Driving Car Nano-degree - Udacity
 *  Created on: December 11, 2020
 *      Author: Mathilde Badoual
 **********************************************/

#include "pid_controller.h"
#include <vector>
#include <iostream>
#include <math.h>

using namespace std;

PID::PID() {}

PID::~PID() {}

void PID::Init(double Kpi, double Kii, double Kdi, double output_lim_maxi, double output_lim_mini) {
   /**
   * TODO: Initialize PID coefficients (and errors, if needed)
   **/
  k_p = Kpi;
  k_i = Kii;
  k_d = Kdi;

  upper_limit = output_lim_maxi;
  lower_limit = output_lim_mini;

  p_err = 0.;
  i_err = 0.;
  d_err = 0.;

  dt = 0.;
}


void PID::UpdateError(double cte) {
   /**
   * TODO: Update PID errors based on cte.
   **/
   // Calculate the difference in error between
   // previous and the current value 
   const double d_cte = cte - p_err;

   p_err = cte;
   d_err = (dt > 0.) ? (d_cte / dt) : 0.;
   i_err += cte * dt;
}

double PID::TotalError() {
   /**
   * TODO: Calculate and return the total error
    * The code should return a value in the interval [output_lim_mini, output_lim_maxi]
   */
    double control = k_p * p_err + k_d * d_err + k_i * i_err;
    if (control > upper_limit)
    {
      return upper_limit;
    }
    else if (control < lower_limit)
    {
      return lower_limit;
    }
    return control;
}

double PID::UpdateDeltaTime(double new_delta_time) {
   /**
   * TODO: Update the delta time with new value
   */
  dt = new_delta_time;
  return dt;
}
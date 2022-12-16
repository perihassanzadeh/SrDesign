#ifndef Motor_h
#define Motor_h
#include <Arduino.h>

class Motor {
public:
  Motor(bool a2, bool a1, bool a0);
  Motor(bool a2, bool a1, bool a0, double percentage, double degrees);
  void setSpeed(double percentage);
  void setDegrees(double degrees);
	void rotate(bool dir);

private:
	bool a2EN;
  bool a1EN;
  bool a0EN;
	double highTime;
  int stepCount;
};

#endif

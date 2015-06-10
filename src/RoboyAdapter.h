/*
 * RoboyAdapter.h
 *
 *  Created on: 10.06.2015
 *      Author: bruh
 */

#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>

#ifndef SRC_ROBOYADAPTER_H_
#define SRC_ROBOYADAPTER_H_

class RoboyAdapter
{
private:
	int socketfd = 0;
	struct sockaddr_in serverAddress;
	int port = 0;
	char buffer[256];

public:
	RoboyAdapter(int port = 22222, std::string inetAddress = "127.0.0.1");
	~RoboyAdapter();

	bool sendSteerHeadMessage(int yaw, int tilt, int roll);

private:

};

#endif /* SRC_ROBOYADAPTER_H_ */

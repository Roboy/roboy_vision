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

public:
	RoboyAdapter(std::string inetAddress = "127.0.0.1", int port = 30000);
	~RoboyAdapter();

	bool sendSteerHeadMessage(int roll, int pitch, int yaw) const;

private:

};

#endif /* SRC_ROBOYADAPTER_H_ */

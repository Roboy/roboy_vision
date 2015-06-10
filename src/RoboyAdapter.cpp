/*
 * RoboyAdapter.cpp
 *
 *  Created on: 10.06.2015
 *      Author: bruh
 */

#include "RoboyAdapter.h"

RoboyAdapter::RoboyAdapter(int port, std::string inetAddress)
{
	int ret = 0;

	this->socketfd = 0;
	this->port     = port;

	memset(&serverAddress, 0x00, sizeof(struct sockaddr_in));

	bzero(buffer, 256);

	serverAddress.sin_family = AF_INET;
	serverAddress.sin_port = htons(port);
	serverAddress.sin_addr.s_addr = inet_addr(inetAddress.data());

	socketfd = socket(AF_INET, SOCK_STREAM, 0);
	if (socketfd < 0) {
		printf("ERROR opening socket\n");
	}

	ret = connect(socketfd, (struct sockaddr *) &serverAddress, sizeof(serverAddress));
	if ( ret > 0) {
		printf("ERROR connecting\n");
	}
}

RoboyAdapter::~RoboyAdapter()
{
	close(socketfd);
}

bool RoboyAdapter::sendSteerHeadMessage(int yaw, int tilt, int roll)
{
	int ret = 0;
	bzero(buffer, 256);

	sprintf(buffer, "%s:%i:%i:%i\n", "head", yaw, tilt, roll);

	printf("Bytes to Write to Stream: %lu\n", strlen(buffer));

	ret = write(socketfd, buffer, strlen(buffer));
	if (ret == -1) {
		printf("ERROR writing data to stream\n");
		return false;
	}
	printf("%i Bytes written to socket\n", ret);
	return true;
}

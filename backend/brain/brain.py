# def main():
#     self.brain_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     self.brain_socket.bind((socket.gethostname(), 9000))
#     self.brain_socket.listen(1)
#     while(True):
#         self.server, _ = self.brain_socket.accept()
#         self.server.recv()
#         if recv == 'hint':
#             send_to_robot('hint')
#
#
# if __name__ == '__main__':
#     main()
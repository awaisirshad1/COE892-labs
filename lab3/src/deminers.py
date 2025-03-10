import ast

import pika
import rover_utils as rvr


class deminer:
    def __init__(self):
        # rabbit setup
        self.rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.rabbit_channel = self.rabbit_connection.channel()
        self.exchange_name = 'lab3'
        self.rabbit_channel.exchange_declare(exchange=self.exchange_name, exchange_type='direct', durable=True)
        self.defuse_routing_key = 'defuse_info'
        self.demine_routing_key = 'demine_info'
        self.demine_queue_name = 'demine_queue'
        self.defuse_queue_name = 'defused_mines'
        self.demine_sub_queue = self.rabbit_channel.queue_declare(queue=self.demine_queue_name, durable=True)
        self.defuse_pub_queue = self.rabbit_channel.queue_declare(queue=self.defuse_queue_name, durable=True)
        self.rabbit_channel.queue_bind(exchange=self.exchange_name, queue=self.demine_queue_name, routing_key=self.demine_routing_key)
        self.rabbit_channel.queue_bind(exchange=self.exchange_name, queue=self.defuse_queue_name, routing_key=self.defuse_routing_key)
        self.cached_mine_ids_serials_pins = {}
        # self.demine_subscriber_queue
        # self.defused_publisher_queue, self.defuse_p_string = self.setup_publish()
        self.demine_numbers = [1, 2]


    def deminer_callback(self, ch, method, properties, body):
        # print(f'\tch:{ch}\n\tmethod:{method}\n\tbody:{body}\n\tproperties:{properties}')
        msg = body.decode('utf-8')
        msg = msg.replace('CLIENT: ', '')
        msg_parts = msg.split(',')
        msg_parts[3] = msg_parts[3] + ',' + msg_parts[4].strip()
        msg_parts.pop()
        msg_dict = {
            msg_parts[0].split('=')[0]: int(msg_parts[0].split('=')[1]),
            msg_parts[1].split('=')[0]: int(msg_parts[1].split('=')[1]),
            msg_parts[2].split('=')[0]: msg_parts[2].split('=')[1],
            msg_parts[3].split('=')[0]: ast.literal_eval(msg_parts[3].split('=')[1])
        }
        print(f'deminer received request from rover with following properties: {msg_dict}\n computing pin...')
        rover_num = msg_dict['rover_number']
        serial_no = msg_dict['serial_number']
        computed_pin = rvr.compute_pin_for_given_mine_sequential(serial_no)
        coords = msg_dict['coordinates']
        published_msg = f'Deminer computed pin={{{computed_pin}}} for rover number={{{rover_num}}} that encountered mine serial number={{{serial_no}}} at coordinates{{{coords}}}'
        print(f'message to publish to ground control: {published_msg}')
        self.rabbit_channel.basic_publish(exchange=self.exchange_name, routing_key=self.defuse_routing_key, body=published_msg)


    def main(self):
        # loop and take inputs
        while (True):
            uinput = input('Enter the deminer number (1/2),  enter \'exit\' to exit:')
            deminer_number = int(uinput)
            if deminer_number not in self.demine_numbers:
                print('incorrect demine number or input, please try again')
                continue
            elif str(uinput).lower() == 'exit':
                print('Goodbye!')
                break
            print(f'running deminer {deminer_number}...')
            self.rabbit_channel.basic_consume(queue=self.demine_queue_name,on_message_callback=self.deminer_callback, auto_ack=True)
            print('starting consumer...')
            self.rabbit_channel.start_consuming()
        self.rabbit_connection.close()


if __name__ == '__main__':
    deminer_obj = deminer()
    deminer_obj.main()
import pygame
import threading
import queue
from net import Net

# Pygame setup
pygame.init()
screen_size = 600
WHITE = (255, 255, 255)
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("OSPF Network Simulation")

# Colors and font
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
font = pygame.font.Font(None, 36)
shortest_path = []
# Initialize network and command queue
net = Net()
router_positions = {}
command_queue = queue.Queue()

def draw_network():
    screen.fill(WHITE)
    drawn_links = set()

    # Draw all links
    for router_id, links in net.graph.lsdb.items():
        for adjacent_router, _ in links.items():
            if (router_id, adjacent_router) not in drawn_links and \
               (adjacent_router, router_id) not in drawn_links:
                # Determine the color based on whether the link is in the shortest path
                color = RED if is_link_in_shortest_path(router_id, adjacent_router) else BLACK
                pygame.draw.line(screen, color, router_positions[router_id], router_positions[adjacent_router], 2)
                drawn_links.add((router_id, adjacent_router))

    # Draw routers
    for router_id, position in router_positions.items():
        pygame.draw.circle(screen, BLUE, position, 20)
        text = font.render(str(router_id), True, WHITE)
        text_rect = text.get_rect(center=position)
        screen.blit(text, text_rect)

    pygame.display.update()

def is_link_in_shortest_path(router1_id, router2_id):
    # Check if a link is part of the shortest path
    for i in range(len(shortest_path) - 1):
        if (shortest_path[i] == router1_id and shortest_path[i + 1] == router2_id) or \
           (shortest_path[i] == router2_id and shortest_path[i + 1] == router1_id):
            return True
    return False



def process_command(command):
    global shortest_path
    args = command.split()
    if args[0] == 'add' and len(args) == 4:
        # Add router with user-defined position
        router_id, x, y = int(args[1]), int(args[2]), int(args[3])
        net.add_router(router_id)
        router_positions[router_id] = (x, y)
        draw_network()  # Update the display after adding a router
    elif args[0] == 'link' and len(args) == 3:
        # Link routers
        router1_id, router2_id = int(args[1]), int(args[2])
        net.add_link(router1_id, router2_id)
        draw_network()  # Update the display after linking routers
    elif args[0] == 'ping' and len(args) == 3:
        # Ping routers
        start_id, end_id = int(args[1]), int(args[2])
        shortest_path = net.ping(start_id, end_id)
        print(f"Path: {shortest_path}")
        draw_network()

def user_input_thread(command_queue):
    while True:
        command = input("Enter command (add, link, ping, exit): ").strip().lower()
        command_queue.put(command)
        if command == "exit":
            pygame.quit()
            return

def main():
    input_thread = threading.Thread(target=user_input_thread, args=(command_queue,))
    input_thread.start()

    running = True
    draw_network()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try:
            command = command_queue.get_nowait()
            if command == "exit":
                running = False
            else:
                process_command(command)
        except queue.Empty:
            pass

        pygame.time.wait(10)

    input_thread.join()

if __name__ == "__main__":
    main()
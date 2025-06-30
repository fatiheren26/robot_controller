ROS2 ile Engelsiz Ortamda TurtleBotu Hedefe Götürme

Çalıştırmak için:
1. TurtleBot3'ün Gazebo ortamında çalışır durumda olması gerekir.
2. `move_node.py` dosyasını bir ROS 2 paketi içinde `src/` klasörüne ekleyin.
3. `colcon build` komutu ile paketi derleyin.
4. Aşağıdaki komutla node'u çalıştırın:

```bash
ros2 run automatic_mover move_node

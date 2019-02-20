# Holds (neighbour, transport) tuple-lists on index == starting point
# Example: node 1 is connected with node 3 by a bus line => CONNECTIONS[1] = (3, 'bus')
# TODO: complete data using physical board (199 nodes) -> convention: first taxi, then bus, then underground
CONNECTIONS = [
    None,  # Index 0 probably not used by physical board?
    [(8, 'taxi'), (9,'taxi'), (58, 'bus'), (46, 'bus'), (46, 'underground')],
    [(20,'taxi'), (10, 'taxi')],
    [(11,'taxi'),(12,'taxi'), (4,'taxi'), (22,'bus'), (23, 'bus')],
    [(13,'taxi')], #node (3,'taxi') already defined in CONNECTIONS[3]
    [(15,'taxi'),(16,'taxi')], #5
    [(29,'taxi'),(7,'taxi')],
    [(17,'taxi'),(42,'bus')], 
    [(18,'taxi'),(19,'taxi')],
    [(20,'taxi'),(19,'taxi')],
    [(11,'taxi'), (21,'taxi'), (34, 'taxi')], #10
    [(22,'taxi')],
    [(23,'taxi')],
    [(23,'taxi'),(24,'taxi'),(23,'bus'),(14,'bus'),(25, 'bus'), (46, 'underground'), (67, 'underground'), (89, 'underground')],
    [(25,'taxi'),(15,'taxi'),(15,'bus')],
    [(16,'taxi'),(26,'taxi'),(28,'taxi'),(41,'bus'),(29,'bus')], #15
    [(28,'taxi'),(29,'taxi')],
    [(29,'taxi'),(30,'taxi')],
    [(43,'taxi'),(31,'taxi')],
    [(32,'taxi')],
    [(33,'taxi')], #20
    [(33,'taxi')],
    [], #continue here ( node 22)
    [],
    [],
    [], #25
    [],
    [],
    [],
    [],
    [], #30
    [],
    [],
    [],
    [],
    [], #35
    [],
    [],
    [],
    [],
    [], #40
    [],
    [],
    [],
    [],
    [], #45
    [],
    [],
    [],
    [],
    [], #50
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
]

EDGE_COLORS = {
    'bus': 'r',
    'taxi': 'g',
    'underground': 'b',
}

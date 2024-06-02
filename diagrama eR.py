from graphviz import Digraph

# Create a new Digraph object
dot = Digraph(comment='Modelo Entidad-Relación')

# Adding entities
dot.node('DOCENTE', 'DOCENTE\n- id_docente\n- rut_docente\n- nombre\n- apellido_paterno\n- apellido_materno\n- telefono\n- correo\n- contraseña')
dot.node('Sala', 'Sala\n- id_sala\n- nombre_sala')
dot.node('Taller', 'Taller\n- taller_id\n- nombre\n- horario\n- id_sala\n- id_docente')
dot.node('Clase', 'Clase\n- id_clase\n- taller_id\n- fecha\n- comentario_bitacora')
dot.node('Estudiantes', 'Estudiantes\n- id_estudiante\n- rut_estudiante\n- nombre\n- apellido_paterno\n- apellido_materno\n- curso\n- correo_institucional')
dot.node('Estudiante_Taller', 'Estudiante_Taller\n- id_taller_estudiante\n- id_estudiante\n- taller_id')
dot.node('Asistencia_Estudiante', 'Asistencia_Estudiante\n- id_asistencia\n- id_clase\n- id_estudiante\n- presencia\n- justificacion')

# Adding relationships
dot.edge('DOCENTE', 'Taller', label='1:N')
dot.edge('Sala', 'Taller', label='1:N')
dot.edge('Taller', 'Clase', label='1:N')
dot.edge('Estudiantes', 'Estudiante_Taller', label='1:N')
dot.edge('Taller', 'Estudiante_Taller', label='1:N')
dot.edge('Clase', 'Asistencia_Estudiante', label='1:N')
dot.edge('Estudiantes', 'Asistencia_Estudiante', label='1:N')

# Render and save the diagram
dot.render('/mnt/data/ER_diagram', format='png', cleanup=False)
'/mnt/data/ER_diagram.png'

from scene_title import SceneTitle

scene = SceneTitle()
scene.call()
while True:
    scene = scene.next_scene
    scene.call()

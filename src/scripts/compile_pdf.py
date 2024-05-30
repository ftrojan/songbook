from typeset import utils


name = "rytmus_v_patach"
profile = utils.get_profile(name)
print(profile)
utils.create_pdf(name, profile)

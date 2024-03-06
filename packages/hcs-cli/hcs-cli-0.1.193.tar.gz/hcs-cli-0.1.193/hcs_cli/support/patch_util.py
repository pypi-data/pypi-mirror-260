from hcs_core.ctxp import CtxpException
import hcs_core.ctxp.data_util as data_util


def calculate_patch(original_object: dict, allowed_fields: list, updates):
    patch = {}
    for u in updates:
        k, v = u.split("=")
        field_name = k.split(".")[0]
        if field_name not in allowed_fields:
            raise CtxpException("Not updatable: " + field_name)

        # special handling for applicationProperties
        if field_name == "applicationProperties":
            prop_name = k[k.index(".") + 1 :]
            props = patch.get("applicationProperties")
            # if props
            continue
        else:
            current_value = data_util.deep_get_attr(original_object, k)
            if str(current_value) == str(v):
                continue
            patch[field_name] = original_object[field_name]
            data_util.deep_set_attr(patch, k, v)

    return patch

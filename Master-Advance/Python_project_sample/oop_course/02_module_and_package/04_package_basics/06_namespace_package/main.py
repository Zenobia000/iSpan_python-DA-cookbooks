import sys
sys.path.extend(["path1", "path2"])

import my_namespace.module_a
import my_namespace.module_b

print(my_namespace.module_a.f_a())
print(my_namespace.module_b.f_b())

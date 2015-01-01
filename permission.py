PERMISSION_DELIMITER = "."
PERMISSION_WILDCARD = "*"


class Permission(object):
    """This class represents the most basic permission possible. It has any number of segments, but is fully defined by
    it's name and has no wildcards, so it grants only itself."""

    def __init__(self, name, description=None):
        """Create a Permission object with the specified name and optional description.

        :param name: The string representing the name of the permission. This indicates what the permission grants.
        :param description: A human-readable string describing the abilities this permission grants.
        :rtype: :py:class`Permission` representing the supplied values.
        """

        self.name = name
        self.description = description

    def grants_permission(self, other_permission):
        """Checks whether this permission grants the supplied permission.

        :param other_permission: The permission that we're checking
        :type other_permission: :py:class:`Permission` or :py:class:`basestring`
        :rtype: True or False
        """

        if isinstance(other_permission, basestring):
            other_permission = Permission(name=other_permission)

        if self == other_permission:
            return True

        return False

    def grants_any_permission(self, permission_set):
        """Checks whether this permission grants access to any permission in the supplied set.

        :param permission_set: The set of Permissions that we are checking
        :rtype: True or False
        """

        return any(self.grants_permission(perm) for perm in permission_set)

    @property
    def segments(self):
        """Returns the list of permission segments that compose this permission.

        :rtype: :py:class`list`
        """

        return self.name.split(PERMISSION_DELIMITER)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "{cls}({name}, {desc})".format(cls=self.__class__.__name__, name=self.name, desc=self.description)

    def __hash__(self):
        return 17 * self.name.__hash__() + 19 * self.description.__hash__()


class WildcardPermission(Permission):
    """This class consists of all permissions that are composed of one or more segments which are a wildcard. This
    allows for easily giving multiple permissions of the same form to users, especially when the number of permissions
    is large, infinite, or undetermined."""

    @property
    def is_end_wildcard(self):
        """Returns whether this permission ends in a wildcard. Terminating wildcards are treated differently from other
        wildcards, as they may represent an infinite number of segments rather than just the typical single segment.

        :rtype: True or False
        """

        return self.segments[len(self.segments)-1] == PERMISSION_WILDCARD

    def grants_permission(self, other_permission):
        """Checks whether this permission grants the supplied permission.

        :param other_permission: The permission that we're checking
        :type other_permission: :py:class:`Permission` or :py:class:`basestring`
        :rtype: True or False
        """

        if isinstance(other_permission, basestring):
            other_permission = WildcardPermission(name=other_permission)

        if len(self.segments) < len(other_permission.segments) and not self.is_end_wildcard:
            return False

        if len(self.segments) > len(other_permission.segments):
            return False

        for s, o in zip(self.segments, other_permission.segments):
            if s != o and s != PERMISSION_WILDCARD:
                return False

        return True


class PermissionSet(set):

    def grants_permission(self, other_permission):
        """Checks whether this permission set has a permission that grants the supplied permission.

        :param other_permission: The permission that we're checking
        :type other_permission: :py:class:`Permission` or :py:class:`basestring`
        :rtype: True or False
        """
        return any(perm.grants_permission(other_permission) for perm in self)

    def grants_any_permission(self, permission_set):
        """Checks whether this permission set has any permission that grants access to any permission in the supplied
        set.

        :param permission_set: The set of Permissions that we are checking
        :rtype: True or False
        """

        """O(n^2) :( Can be done faster."""
        return any(self.grants_permission(perm) for perm in permission_set)

    def has_any_permission(self, other_permission):
        """Checks whether any permission in this permission set is of the form other_permission. Strictly speaking, this
        checks whether any permission in the set is granted by other_permission.

        :param other_permission: The permission whose form we're checking for
        :rtype: True or False
        """

        if isinstance(other_permission, basestring):
            other_permission = WildcardPermission(name=other_permission)

        return other_permission.grants_any_permission(self)

    def __getattr__(self, item):
        ret = getattr(super(PermissionSet, self), item)
        return PermissionSet(ret) if isinstance(ret, set) else ret



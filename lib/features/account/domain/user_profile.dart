/// `GET /me`
class UserProfile {
  const UserProfile({
    required this.uid,
    required this.email,
    required this.displayName,
    required this.onboardingCompleted,
  });

  final String uid;
  final String? email;
  final String? displayName;
  final bool onboardingCompleted;

  factory UserProfile.fromJson(Map<String, dynamic> json) => UserProfile(
    uid: json['uid'] as String,
    email: json['email'] as String?,
    displayName: json['display_name'] as String?,
    onboardingCompleted: json['onboarding_completed'] as bool,
  );

  Map<String, dynamic> toJson() => {
    'uid': uid,
    'email': email,
    'display_name': displayName,
    'onboarding_completed': onboardingCompleted,
  };
}

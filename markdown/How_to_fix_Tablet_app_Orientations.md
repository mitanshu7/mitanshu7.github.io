---
title: "How to fix Tablet app Orientations"
description: "Force portrait-locked apps like Venmo or Authy to run in landscape on Android tablets and foldables using a simple ADB command. Works on Android 12+ with letterboxing support."
---

## Free the portrait

**Mitanshu Sukhwani** • _07 June 2025_

Following is a copy of the [Reddit post](https://www.reddit.com/r/Android/comments/13c4pum/tutorial_how_to_stop_apps_like_authy_venmo_etc/) by [u/MishaalRahman](https://www.reddit.com/user/MishaalRahman/):

**Tutorial**: _How to stop apps like Authy, Venmo etc. from being locked to portrait mode on Android tablets/foldables_

One of the most annoying parts about using most Android tablets or foldables is being forced to flip the device over because an app doesn't support landscape mode. This is a big issue on the OPPO Find N2, for example. [Fortunately, there's a fix. Here's how it works.](https://pbs.twimg.com/media/FvoVWk9aQAIai5S?format=jpg&name=4096x4096)

If you aren't familiar with this problem or don't think it's a big deal, watch [this part of Michael Fisher's OPPO Find N2 review](https://www.youtube.com/watch?v=43J5QEF5w8Y&t=265s). The Find N2 has a "widebody" inner screen that defaults to landscape mode. As Michael points out, lots of folks (myself included) think the "widebody" approach to foldables is better. But as you can see, it's not always perfect. Apps like BeReal, Authy, Venmo, Zipcar, Lyft, Delta, Chase, & Amex are locked to portrait mode, forcing you to rotate the phone after unfolding it.

This issue also affects tablets like the new OnePlus Pad, by the way! In fact, this problem has affected large screen Android devices for years now, and Google quietly implemented a way for OEMs to fix this...though none of them are using it yet.

# Background

But first, why does this happen? It's not exactly Google/Android or the OEMs' faults. It's more to do with the decisions of app developers, as many apps just aren't optimized for large screen devices.

Now, Google has always recommended that developers design their apps with responsive layouts that make full use of the screen space available in both portrait and landscape orientations on large screen devices. But they don't mandate this.

Given that traditional candybar phones dominate the market and tablets/foldables are sold in far fewer quantities, it makes sense that most Android apps are optimized for candybar phones in portrait mode. Supporting other form factors requires additional work. It's gotten easier over the years to do so, but it's still more work.

What should devs whose apps aren't landscape-optimized do when a tablet user wants to use their app in that orientation? "Optimize the app for large screens" is preferable but they may not have the time/resources/sign-off. So to keep the app looking/working as intended, just lock it to portrait mode!

Setting the [android:screenOrientation](https://pbs.twimg.com/media/Fvoa9MwaQAAqKrn?format=jpg&name=large) attribute to "portrait" on any activity will make Android rotate the screen to portrait when that activity is visible. Apps like Authy, BeReal, Venmo use this. There's also [an API](https://pbs.twimg.com/media/FvobohsaAAE6ryc?format=jpg&name=large) to programmatically change the orientation, which some use.

It's obviously not ideal that there are so many apps that aren't optimized for landscape/large screen devices. Forcing devs to support them would be a huge burden and hard to justify given current market share, though, so Google doesn't do that.

# The solution

That's why Google made a solution that both respects that some devs don't want their apps to be stretched and lets OEMs decide how they want apps to be shown. OEMs can [override apps' orientation preferences](https://pbs.twimg.com/media/Fvof0ezaQAIZ8TG?format=jpg&name=large) and display them in a letterbox that maintains the aspect ratio.

This feature was added in Android 12, as I mentioned in [my Android 12L deep dive for Esper.io](https://blog.esper.io/android-12l-deep-dive/#android12l_orientationoverride). My article also pointed out that there's a shell command that AOSP engineers can use to test this feature. That's what we'll take advantage of here!

All you have to do to fix this issue on your own device is to run a command to tell Android to ignore apps' orientation preferences on a particular display. For the OnePlus Pad/OPPO Find N2's main display, for example, the command is as follows:

```bash
adb shell wm set-ignore-orientation-request -d 0 true
```

Display ID '0' might not be the right display ID for your foldable's inner display, so you may need to substitute '0' with another number. Use the command `adb shell cmd display get-displays` to see the list of displays.

This command should take effect immediately, though you may need to close out of an app and then relaunch it. Here are photos of the Venmo app running in a letterbox on the [OPPO Find N2](https://pbs.twimg.com/media/Fvohe2DaIAE2jBg?format=jpg&name=large) and [OnePlus Pad](https://pbs.twimg.com/media/Fvohe3KaQAAI5ux?format=jpg&name=large) after applying this fix.

(📷 credits: Tim Schofield)

As you can see, the Venmo app isn't stretched out - respecting its devs' desire to have it be presented in a particular aspect ratio while also letting you use it in a more natural orientation. The solid gray background could be made better, but unfortunately, not on ColorOS.

While Android 12 added [letterboxing customization](https://blog.esper.io/android-12l-deep-dive/#android12l_betterletterboxing)—where to place the app (eg. left instead of center) or what the background should look like—on some OEM forks of Android, the letterboxing shell commands were removed, so you can't adjust this yourself.

In any case, I hope this trick helps! Big thanks to @qbking77 for testing this and sending me the photos. Try this out if you have a tablet or foldable running Android 12 or later!

If you're running < Android 12, try the app [Rotation | Orientation Manager](https://play.google.com/store/apps/details?id=com.pranavpandey.rotation) on Google Play (or a similar app). These apps use Android's Accessibility API to display an invisible, noninteractive overlay that requests your desired orientation. It's not perfect but it may work for you!

**Last bit**: If you're wondering why OPPO/OnePlus doesn't use this feature, it could be they decided forced portrait provides a better experience than a customized letterbox (I'd disagree with that). Or it could be they just don't know it exists! After all, it's not like OEMs magically know about every single little thing that Google adds to each new Android version! They get told a lot of things, but often still have to dig into each release to assess minor changes/features like I do :)

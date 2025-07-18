
Pod::Spec.new do |s|
  s.name             = 'MyLibary'
  s.version          = '0.1.0'
  s.summary = 'A brief description of MyLibary'
  s.description      = <<-DESC
TODO: Add long description of the pod here.
                       DESC
  s.homepage         = 'https://git.ninebot.com/'
  s.license          = { :type => 'MIT', :file => 'LICENSE' }
  s.author           = { 'ninebot' => 'www.ninebot.com' }
  s.source           = { :git => 'https://git.ninebot.com/iOS/MyLibary.git', :tag => s.version.to_s }

  s.ios.deployment_target = '13.0'
  s.source_files = 'MyLibary/Sources/**/*'
  

  type = ENV['type'] == 'overseas' ? 'Overseas' : 'China'
  s.resource_bundles = {
    'MyLibary' => ["MyLibary/Resources/#{type}/**/*.*"]
  }

  
  # s.frameworks = 'UIKit', 'MapKit'
  # s.dependency 'AFNetworking', '~> 2.3'
end
